-- Native B42 Mod Options persist these preferences locally, outside save data.
require "PZAPI/ModOptions"

local page, enabledOption, effectsOption, ambienceOption
local gains = { 0, 0.5, 1, 1.5, 2, 3, 4, 6, 8, 12, 16 }
local bridgeWarningShown = false

-- Read option indices defensively. Old/corrupt indices fall back to unity.
local function selectedGain(option)
    return gains[tonumber(option:getValue()) or 0] or 1
end

-- Applies saved local choices through the registered Java bridge. Does not edit
-- vanilla volume settings. The native helper checks camera mode at playback time.
local function applyOptions()
    if not page then return end
    local bridge = ViewpointAudioBalance
    if not bridge or not bridge.configure then
        if not bridgeWarningShown then
            print("[VAB] Java settings bridge unavailable; gain remains unchanged."
                .. " Check ZombieBuddy loading and restart the game fully.")
            bridgeWarningShown = true
        end
        return
    end
    local ok, err = pcall(bridge.configure, enabledOption:getValue() == true,
        selectedGain(effectsOption), selectedGain(ambienceOption))
    if not ok then
        print("[VAB] Could not apply local options: " .. tostring(err))
    end
end

-- Adds one native combobox. 2x is the initial trial gain for both independent
-- groups; 1x bypasses gain, 0 mutes the selected group only in Viewpoint 3D.
local function addGainOption(id, label, tooltip)
    local option = page:addComboBox(id, label, tooltip)
    for _, gain in ipairs(gains) do
        local text = gain == 0 and "Muted" or (tostring(gain) .. "x")
        if gain == 1 then text = text .. " (unchanged)" end
        option:addItem(text, gain == 2)
    end
    return option
end

-- Installs once per Lua environment, using the game's built-in Mod Options API.
-- This is an options page, not an extra Mod Options Workshop dependency.
local function install()
    if page or not (PZAPI and PZAPI.ModOptions) then return end
    page = PZAPI.ModOptions:create("ViewpointAudioBalance", "Viewpoint - Audio Balance")
    page:addTitle("First- and third-person audio")
    page:addDescription("Applies while Viewpoint 3D is active. Start with a lower"
        .. " output volume when testing gain. Isometric gain is unchanged.")
    enabledOption = page:addTickBox("Enabled", "Enable Viewpoint audio balance", true)
    effectsOption = addGainOption("EffectsGain", "World effects gain",
        "Footsteps, doors, combat, zombie voices and other world effects."
        .. " Music and UI sounds bypass this control.")
    ambienceOption = addGainOption("AmbienceGain", "Background ambience gain",
        "The game's Ambient group: includes the combined day/night/weather"
        .. " soundscape and ambient hums. This is independent of world effects;"
        .. " individual layers inside one FMOD event are not split.")
    page.apply = applyOptions
    print("[VAB] Native Mod Options page registered.")
end

-- Reload persisted settings before the first in-world apply. No OnTick handler.
local function onGameStart()
    install()
    if page then
        local ok, err = pcall(function() PZAPI.ModOptions:load() end)
        if not ok then print("[VAB] Saved options could not load: " .. tostring(err)) end
        applyOptions()
    end
end

install()
Events.OnGameBoot.Add(install)
Events.OnGameStart.Add(onGameStart)
