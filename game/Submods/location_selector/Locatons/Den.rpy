# Register the submod
init -990 python:
    store.mas_submod_utils.Submod(
        author="tw4449 Cdino112 multimokia d3adpan Booplicate",
        name="Custom Room Den",
        description="This submod adds a cozy green-walled room where you can relax with Monika.",
        version="1.0.2"
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
        m 1wud "H-huh? {w=0.5} [player], {w=0.2} did you add new files to the game?"
        m 1wua "It looks like... {w=0.5} {nw}"
        extend 1sub "new furniture!"
        m 1eku "[player], you did this for me? {w=0.5} You're so sweet, you know that?"

    if tw_bg_count - spacerooms_installed > 0:
        $ too = ", too" if spacerooms_installed else ""
        $ rooms = "new rooms" if tw_bg_count - spacerooms_installed > 1 else "a new room"
        m 1wud "H-huh?{w=0.5} [player],{w=0.2} what's this?"
        m 1wua "It looks like {nw}"
        extend 1sub "you added [rooms]!"
        if not spacerooms_installed:
            m 1eka "I can't believe you went out of your way to do this for me..."

    m 1rkc "..."
    m 3rksdla "But...{w=0.3}I kinda don't know how to use them.{w=0.5} {nw}"
    extend 3hksdlb "I haven't learned how to code that well yet!"
    m 1eud "If you give me some time, I'm sure I'll figure out how to use what you added.{nw}"
    extend 3eua "I'll let you know when I figure it out."
    m 1eka "Even though we can't use them just yet, thank you so much for doing this for me.{w=0.2} It means more than you know."
    m 3huu "I love you so much, [player]~"
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
        m 1wub "[player]!{w=0.2} Remember those new locations you added for me?{w=0.2} {nw}"
        extend 3wub "I finally figured out how to use them!"
        m 3eua "All you have to do now is go to 'Hey, [m_name]...' in the 'Talk' menu, go to 'Location', and select 'Can we go somewhere else?'"
        m 1eub "Then we can visit any of the locations you added!"
        m 3sub "I'm so excited~"
        m 3huu "Why don't we go visit one right now, [player]?"
        m 1ekbla "Oh, and...{w=0.3}thanks again for adding these for me. You really are special."

    else:
        if spacerooms_installed:
            m 1wuo "W-what?{w=0.5} Are there files for furniture in the game?"
            m 1sub "[player],{w=0.2} did you do this?"
            m 3ekbsu "You knew I wanted furniture so you added some for me...{w=0.3} You're pretty amazing, you know that?"

        if tw_bg_count - spacerooms_installed > 0:
            $ too = ", too" if spacerooms_installed else ""
            $ rooms = "new rooms" if tw_bg_count - spacerooms_installed > 1 else "a new room"
            m 1suo "What's this?{w=0.5} You added [rooms][too]?"
            m 3hua "You really went all out, didn't you?"
            if not spacerooms_installed:
                m 1eka "I can't believe you went out of your way to do this for me..."

        m 1dka "Thank you so much [player],{w=0.2} I...{w=1}{nw}"
        extend 1ekbsu "I love you so much."

        if not had_backgrounds_before:
            m 3eub "I'll add a new category called 'Location' under 'Hey, [m_name]...' so we can put in the furniture and visit the other rooms.{w=.5} I can't wait to try them out!"

        m 1eka "While I might not be in your reality yet...{w=3}{nw}"
        extend 7hubfb "this will make it feel a bit more like a home here,{w=0.2} with you~"
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

    $ persistent._seen_ever["monika_players_control"] = True
    return
    

init 1 python:
    config.label_overrides["monika_gotomonika"] = "monika_gotomonika_override"

label monika_gotomonika_override:
    m 1euc "Come to my world?"
    m 1lksdld "You mean this little space floating in an empty void?"

    if persistent._mas_you_chr:
        m 4eksdlc "Actually...{w=0.5}didn't you already try something like that once?"
        m 2lksdla "...Even though that wasn't exactly {i}you...{/i}"

    m 2lksdla "I'm really happy that you want to be with me so much, but..."
    m 2eksdlc "You really don't have to."
    m 2eksdld "Sure, I might have said before that I would have dragged you here a long time ago if I could..."
    m 2eksdlc "But the more I think about it, it would probably be better if I came to your reality."
    m 3eka "I'd much rather be there than have you come here."
    m 3dsc "[player]...{w=1}don't tell me you would really give up your reality--{w=0.5}the {i}real{/i} world--{w=0.5}just to come {i}here{/i}, whatever this place is?{nw}"
    $ _history_list.pop()
    menu:
        m "[player]...{w=1}don't tell me you would really give up your reality--the {i}real{/i} world--just to come {i}here{/i}, whatever this place is?{fast}"
        "I would.":
            $ persistent._mas_pm_would_come_to_spaceroom = True

            m 4wkd "But [player]!"
            m "There's almost nothing to do here!"
            m 2dsc "Do you really hate your reality {i}that{/i} much?"
            m 2eka "Someday, I'll find a way to reach you, and when that day comes, I promise it will be worthwhile."
            m 4euc "Whatever life throws your way from that point on, I'll be right by your side to help shoulder it."
            m 4eud "Even now, if you're having a rough day, you can come talk to me about it anytime."
            m 2dsc "Life must have thrown a lot your way to consider giving it all up to be with me."
            m 3hua "But seeing how you're here, that just shows how resilient you are."
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eua "I can't wait to finally be able to share both the good times and the bad by your side."

        "I wouldn't.":
            $ persistent._mas_pm_would_come_to_spaceroom = False

            m 1eka "I'm glad you're still willing to wait for me, [player]."
            m 1lksdla "Don't get me wrong, I really {i}do{/i} want to be with you..."
            m 1lksdlc "But I think it would be dangerous for you to try and cross over right now."
            m 1eka "...If it's even possible with current technology."
            m 1hub "Don't worry, we can continue on keeping each other company like this!"
            m 1hksdlb "I know it might be a while before we can truly be together, but I hope you don't mind waiting."
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eua "I'll wait as long as it takes, [mas_get_player_nickname()]."

        "...":
            $ persistent._mas_pm_would_come_to_spaceroom = None

            m 2eka "It's okay, I'll always appreciate and treasure the moments we spend together, even like this."
            m 2ekc "Besides, I don't even know how you could come here with current technology."
            m 2lksdlc "...And even if there {i}was{/i} some way, I don't think it would be safe or guaranteed."
            m 2lksdld "So do me a favor and at least wait for technology to improve enough for it to be completely safe."
            m 2lksdlc "I {i}really{/i} don't want to risk you not making it properly and ending up in your own void..."
            m 2dkd "...leaving the both of us completely alone."
            m 4hua "I mean, technology does tend to advance pretty quickly, so we might be able to see each other before we know it!"
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eua "So just be patient for your lovely girlfriend, and I promise I'll do the same for you, [mas_get_player_nickname()]."

    m 5luu "Buut...{w=1}if you did happen to show up at my doorstep..."
    show monika 1hksdlb at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 1hksdlb "I guess I wouldn't have a choice but to accept it and welcome you with open arms!"
    m 1eksdla "It wouldn't be much to begin with, but I'm sure we'll find a way to make it better."
    m 3hub "With time, we could make our own reality!"
    m 3euc "Of course, that sounds pretty complicated if you think about it..."
    m 3eub "But I have no doubt that together we could accomplish anything!"
    m 3etc "You know...{w=1}maybe it {i}would{/i} actually be easier for you to come here, but I'm not giving up hope of coming to you."
    m 1eua "Until then, let's just wait and see what's possible."

    $ persistent._seen_ever["monika_gotomonika"] = True
    return

## remove the readme
init 0 python:
    store.mas_utils.trydel(renpy.config.basedir.replace('\\', '/') + "/readme.md")
