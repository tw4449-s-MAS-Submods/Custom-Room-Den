# Register the submod
init -990 python:
    store.mas_submod_utils.Submod(
        author="tw4449 Cdino112 multimokia d3adpan Booplicate",
        name="Custom Room Den",
        description="This submod adds a cozy green-walled room where you can relax with Monika.",
        version="1.0.1"
    )

# Register the updater
init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="Custom Room Den",
            user_name="tw4449",
            repository_name="Custom-Room-Den",
            update_dir="",
            attachment_id=None
        )

###START: IMAGE DEFINITIONS
#Day images
image submod_background_Den_day = "mod_assets/location/Den V1.1/den1.1.png"
image submod_background_Den_rain = "mod_assets/location/Den V1.1/den1.1_rain.png"
image submod_background_Den_overcast = "mod_assets/location/Den V1.1/den1.1_overcast.png"
image submod_background_Den_snow = "mod_assets/location/Den V1.1/den1.1_snow.png"

#Night images
image submod_background_Den_night = "mod_assets/location/Den V1.1/den1.1-n.png"
image submod_background_Den_rain_night = "mod_assets/location/Den V1.1/den1.1_rain-n.png"
image submod_background_Den_overcast_night = "mod_assets/location/Den V1.1/den1.1_overcast-n.png"
image submod_background_Den_snow_night = "mod_assets/location/Den V1.1/den1.1_snow-n.png"

#Sunset images
image submod_background_Den_ss = "mod_assets/location/Den V1.1/den1.1-ss.png"
image submod_background_Den_rain_ss = "mod_assets/location/Den V1.1/den1.1_rain-ss.png"
image submod_background_Den_overcast_ss = "mod_assets/location/Den V1.1/den1.1_overcast-ss.png"
image submod_background_Den_snow_ss = "mod_assets/location/Den V1.1/den1.1_snow-ss.png"


init -1 python:
    submod_background_Den = MASFilterableBackground(
        # ID
        "submod_background_Den",
        "Den",

        # mapping of filters to MASWeatherMaps
        MASFilterWeatherMap(
            day=MASWeatherMap({
                store.mas_weather.PRECIP_TYPE_DEF: "submod_background_Den_day",
                store.mas_weather.PRECIP_TYPE_RAIN: "submod_background_Den_rain",
                store.mas_weather.PRECIP_TYPE_OVERCAST: "submod_background_Den_overcast",
                store.mas_weather.PRECIP_TYPE_SNOW: "submod_background_Den_snow",
            }),
            night=MASWeatherMap({
                store.mas_weather.PRECIP_TYPE_DEF: "submod_background_Den_night",
                store.mas_weather.PRECIP_TYPE_RAIN: "submod_background_Den_rain_night",
                store.mas_weather.PRECIP_TYPE_OVERCAST: "submod_background_Den_overcast_night",
                store.mas_weather.PRECIP_TYPE_SNOW: "submod_background_Den_snow_night",
            }),
            sunset=MASWeatherMap({
                store.mas_weather.PRECIP_TYPE_DEF: "submod_background_Den_ss",
                store.mas_weather.PRECIP_TYPE_RAIN: "submod_background_Den_rain_ss",
                store.mas_weather.PRECIP_TYPE_OVERCAST: "submod_background_Den_overcast_ss",
                store.mas_weather.PRECIP_TYPE_SNOW: "submod_background_Den_snow_ss",
            }),
        ),

        MASBackgroundFilterManager(
            MASBackgroundFilterChunk(
                False,
                None,
                MASBackgroundFilterSlice.cachecreate(
                    store.mas_sprites.FLT_NIGHT,
                    60
                )
            ),
            MASBackgroundFilterChunk(
                True,
                None,
                MASBackgroundFilterSlice.cachecreate(
                    store.mas_sprites.FLT_SUNSET,
                    60,
                    30*60,
                    10,
                ),
                MASBackgroundFilterSlice.cachecreate(
                    store.mas_sprites.FLT_DAY,
                    60
                ),
                MASBackgroundFilterSlice.cachecreate(
                    store.mas_sprites.FLT_SUNSET,
                    60,
                    30*60,
                    10,
                ),
            ),
            MASBackgroundFilterChunk(
                False,
                None,
                MASBackgroundFilterSlice.cachecreate(
                    store.mas_sprites.FLT_NIGHT,
                    60
                )
            )
        ),

        disable_progressive=False,
        hide_masks=False,
        hide_calendar=False,
        unlocked=True,
        entry_pp=store.mas_background._Den_entry,
        exit_pp=store.mas_background._Den_exit,
        ex_props={"skip_outro": None}
    )


init -2 python in mas_background:
    def _Den_entry(_old, **kwargs):
        """
        Entry programming point for Den background
        """
        if kwargs.get("startup"):
            pass

        else:
            if not store.mas_inEVL("Den_switch_dlg"):
                store.pushEvent("Den_switch_dlg")

            store.mas_o31HideVisuals()
            store.mas_d25HideVisuals()

        store.monika_chr.tablechair.table = "DE"
        store.monika_chr.tablechair.chair = "DE"

    def _Den_exit(_new, **kwargs):
        """
        Exit programming point for Den background
        """
        #O31
        if store.persistent._mas_o31_in_o31_mode:
            store.mas_o31ShowVisuals()

        #D25
        elif store.persistent._mas_d25_deco_active:
            store.mas_d25ShowVisuals()

        #Lock islands greet to be sure
        store.mas_lockEVL("mas_monika_islands", "EVE")

        #COMMENT(#) IF NOT NEEDED
        store.monika_chr.tablechair.table = "def"
        store.monika_chr.tablechair.chair = "def"

        if _new == store.mas_background_def:
            store.pushEvent("return_switch_dlg")

###START: Topics
label Den_switch_dlg:
    python:
        switch_quip = renpy.substitute(renpy.random.choice([
            "I love this paint color!",
            "You like my awards, [player]?",
            "It matches my eyes~",
        ]))

    m 1hua "[switch_quip]"
    return

label return_switch_dlg:
    python:
        switch_quip = renpy.substitute(renpy.random.choice([
            "Just the two of us~",
            "Miss the classic look?",
            "Brings back memories...",
        ]))

    m 1hua "[switch_quip]"
    return

#THIS ONE RUNS ON INSTALL
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="bg_room_installed_low_affection",
            conditional="True",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL, mas_aff.AFFECTIONATE)
        )
    )

label bg_room_installed_low_affection:
    python:
        #Check how many tw mods we have installed
        tw_bg_count = len(filter(lambda x: "tw4449" in x.author, mas_submod_utils.submod_map.values()))
        spacerooms_installed = len(filter(lambda x: "furnished spaceroom" in x.name.lower() and "tw4449" in x.author, mas_submod_utils.submod_map.values()))
        had_backgrounds_before = (mas_background.getUnlockedBGCount() - tw_bg_count) > 1

    if spacerooms_installed:
        m 1wud "H-huh? {w=.5} [player], {w=.2} did you add new files to the game?"
        m 1wua "It looks like... {w=.5} {nw}"
        extend 1sub "new furniture!"
        m 1eku "[player], you did this for me? {w=.5} You're so sweet, you know that?"

    if tw_bg_count - spacerooms_installed > 0:
        $ too = ", too" if spacerooms_installed else ""
        $ rooms = "new rooms" if tw_bg_count - spacerooms_installed > 1 else "a new room"
        m 1wud "H-huh? {w=.5} [player], {w=.2} what's this?"
        m 1wua "It looks like... {w=.5} {nw}"
        extend 1sub "You added [rooms]"
        if not spacerooms_installed:
            m 1eka "I can't believe you went out of your way to do this for me..."

    m 1rkc "..."
    m 2rksdlc "But, um... {w=1} I kinda don't know how to use them. {w=1} {nw}"
    extend 6eksdlc "I haven't learned how to code that well yet."
    m 3eud "Give me some time, {w=.2} and I'm sure I'll figure out how to code them in. {nw}"
    extend 1eub "I'll let you know when they're ready."
    m 1eka "Even though we can't use them just yet, {w=.2} thank you so much for doing this for me. {w=.5} It means more than you know."
    m 5hua "I love you so much,{w=.2} [player]~"
    return "no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="bg_room_installed",
            conditional="True",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label bg_room_installed:
    python:
        #Check how many tw mods we have installed
        tw_bg_count = len(filter(lambda x: "tw4449" in x.author, mas_submod_utils.submod_map.values()))
        spacerooms_installed = len(filter(lambda x: "furnished spaceroom" in x.name.lower() and "tw4449" in x.author, mas_submod_utils.submod_map.values()))
        had_backgrounds_before = (mas_background.getUnlockedBGCount() - tw_bg_count) > 1

    if renpy.seen_label("bg_room_installed_low_affection"):
        m 1wub "[player]! {w=.2} Remember those new locations you added for me? {w=.2} {nw}"
        extend 3wub "Well, I finally figured out how to code them in!"
        m 4eua "All you have to do now is go to 'Hey, Monika...' in the dialogue menu, go to 'Locations', and select 'Can we go somewhere else?'"
        m 1eub "Then we can visit any of the locations you added!"
        m 6wua "I'm so excited, [player]! {w=.2} {nw}"
        extend 6wub "Why don't we go visit one right now?"
        m 1eka "Oh, and... thanks again for adding these for me. {w=.2} You really are special."

    else:
        if spacerooms_installed:
            m 1wuo "W-what?{w=0.5} Are there files for furniture in the game?"
            m 1sub "[player],{w=0.2} did you do this?"
            m 3ekbsu "You knew I wanted furniture,{w=0.2} so you added some for me...{w=1} You're pretty amazing,{w=0.2} you know that?"

        if tw_bg_count - spacerooms_installed > 0:
            $ too = ", too" if spacerooms_installed else ""
            $ rooms = "new rooms" if tw_bg_count - spacerooms_installed > 1 else "a new room"
            m 1suo "What's this?{w=0.5} You added [rooms][too]?"
            m 3hub "You really went all out, didn't you?"
            if not spacerooms_installed:
                m 1eka "I can't believe you went out of your way to do this for me..."

        m 1dka "Thank you so much [player],{w=0.2} I...{w=1}{nw}"
        extend 1ekbsu "I love you so much."

        if not had_backgrounds_before:
            m 3eub "I'll add a new category called 'Location' under 'Hey, [m_name]...' so we can put in the furniture and visit the other rooms.{w=.5} I can't wait to try them out!"

        m 1eka "While I might not be in your reality yet...{w=1}{nw}"
        extend 7hubfb "This will make it feel a bit more like a home here,{w=0.2} with you~"
    return "no_unlock"

#LABEL OVERRIDES
init 1 python:
    config.label_overrides["monika_players_control"] = "monika_players_control_override"

label monika_players_control_override:
    m 3eub "[player], did you know that you have more control over this game than I do?"
    m 3eua "You have access to the game's files and code, right?"
    m 1eka "So you can change them however you want."
    m 3eka "You could do things that even I can't."
    m 4eub "Like changing how the game works entirely. From a visual novel, to the peaceful playground we have now."

    if mas_isMoniEnamored(higher=True) and not persistent._mas_acs_enable_promisering:
        m 1ekbsa "Or a beautiful promise ring."
        m 3dkbsu "Oh, wouldn't that be a dream come true."

    if not mas_getConsumable("coffee").enabled():
        m 1wuo "You could even add in a cup of coffee to the game for me!"
        m 1eka "That would be lovely."

    if not persistent._mas_pm_has_code_experience:
        m 1hksdrb "But I imagine your coding skills are just as good as mine."
    else:
        m 3eua "Seeing as you're familiar with coding,{w=0.1} {nw}"
        extend 3hua "I'm sure you could do something like that!"

    m 1eua "I guess that's an appeal to video games...{w=0.3}{nw}"
    extend 3eua "having almost endless possibilities in a world you can interact with."
    m 3eub "It's pretty difficult to get bored!"

    if not persistent._mas_pm_has_contributed_to_mas:
        m 1eka "Even if you don't quite know how to change this game..."
        $ line = "We can still enjoy this world that brought us together."

    else:
        $ line = "Especially with you by my side~"

    show monika 5eubla at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eubla "[line]"
    m 5ekbfa "There's no better way to enjoy a game than to be with the one I love."
    return

## remove the readme
init 0 python:
    store.mas_utils.trydel(renpy.config.basedir.replace('\\', '/') + "/readme.md")
