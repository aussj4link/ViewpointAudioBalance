#!/usr/bin/env python3
"""Check Lua options lifecycle using Lua 5.4 and minimal native-API stand-ins."""
import ctypes
import ctypes.util
from pathlib import Path


def main():
    library = ctypes.util.find_library("lua5.4")
    if not library:
        raise SystemExit("Lua 5.4 shared library required for these local checks.")
    lua = ctypes.CDLL(library)
    lua.luaL_newstate.restype = ctypes.c_void_p
    lua.luaL_openlibs.argtypes = [ctypes.c_void_p]
    lua.luaL_loadstring.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    lua.lua_pcallk.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int,
                             ctypes.c_int, ctypes.c_longlong, ctypes.c_void_p]
    lua.lua_tolstring.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]
    lua.lua_tolstring.restype = ctypes.c_char_p
    lua.lua_close.argtypes = [ctypes.c_void_p]
    state = lua.luaL_newstate()
    lua.luaL_openlibs(state)

    def execute(source):
        if lua.luaL_loadstring(state, source.encode()) or lua.lua_pcallk(state, 0, 0, 0, 0, None):
            raise AssertionError(lua.lua_tolstring(state, -1, None).decode())

    try:
        execute('''
        package.preload["PZAPI/ModOptions"] = function() return true end
        local function event()
            local result = { callbacks = {} }
            result.Add = function(callback) table.insert(result.callbacks, callback) end
            return result
        end
        Events = { OnGameBoot = event(), OnGameStart = event() }
        PZAPI = { ModOptions = { creates = 0, loads = 0 } }
        function PZAPI.ModOptions:create(id, name)
            self.creates = self.creates + 1
            local page = { options = {} }
            function page:addTitle(text) end
            function page:addDescription(text) end
            function page:addTickBox(id, label, initial)
                local option = { value = initial }
                function option:getValue() return self.value end
                self.options[id] = option
                return option
            end
            function page:addComboBox(id, label, tooltip)
                local option = { items = {}, selected = 1 }
                function option:addItem(text, selected)
                    table.insert(self.items, text)
                    if selected then self.selected = #self.items end
                end
                function option:getValue() return self.selected end
                self.options[id] = option
                return option
            end
            self.page = page
            return page
        end
        function PZAPI.ModOptions:load()
            self.loads = self.loads + 1
            if self.saved then
                self.page.options.EffectsGain.selected = self.saved[1]
                self.page.options.AmbienceGain.selected = self.saved[2]
            end
        end
        configured = {}
        ViewpointAudioBalance = { configure = function(enabled, fx, ambient)
            configured[#configured + 1] = { enabled, fx, ambient }
        end }
        ''')
        script = Path(__file__).resolve().parents[1] / "42/media/lua/client/VAB_Options.lua"
        execute(script.read_text())
        execute('''
        local api = PZAPI.ModOptions
        assert(api.creates == 1)
        assert(api.page.options.EffectsGain.selected == 5)
        assert(api.page.options.AmbienceGain.selected == 5)
        for _, callback in ipairs(Events.OnGameBoot.callbacks) do callback() end
        assert(api.creates == 1, "duplicate options page")
        api.saved = { 7, 2 } -- 4x effects, 0.5x ambience
        for _, callback in ipairs(Events.OnGameStart.callbacks) do callback() end
        assert(api.loads == 1)
        assert(configured[1][1] and configured[1][2] == 4 and configured[1][3] == 0.5)
        api.page.options.Enabled.value = false
        api.page.apply()
        assert(configured[2][1] == false, "checkbox bypass")
        api.page.options.EffectsGain.selected = 999
        api.page.apply()
        assert(configured[3][2] == 1, "invalid selection fallback")
        ViewpointAudioBalance = nil
        api.page.apply()
        api.page.apply()
        assert(#configured == 3, "missing bridge changed state")
        print("PASS Lua syntax, defaults, idempotent install, saved choices, apply,"
            .. " disabled state, invalid selection and missing-bridge checks.")
        ''')
    finally:
        lua.lua_close(state)


if __name__ == "__main__":
    main()
