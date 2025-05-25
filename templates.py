templates = [

"""
    public static final Item MUSIC_DISC_{name_capital} = registerItem(
        "music_disc_{name}",
         new Item.Settings().rarity(net.minecraft.util.Rarity.RARE)
            .jukeboxPlayable(ModSounds.{name_capital}_KEY).maxCount(1)
    );

""",

"""
    public static final SoundEvent {¨name_capital} = registerSoundEvent("{name}");
    public static final RegistryKey<JukeboxSong> {name_capital}_KEY =
        RegistryKey.of(RegistryKeys.JUKEBOX_SONG, Identifier.of(AnthemDiscs.MOD_ID, "{name}"));

""",

"""
    "item.anthemdiscs.music_disc_name": "Music Disc",
    "item.anthemdiscs.music_disc_name.desc": "National Anthem - {name_first_capital}",

""",

"""
      "{name}": {
        "sounds": [
          {
            "name": "anthemdiscs:{name}",
            "stream": true
          }
        ]
      }
    }

"""

]

templates_single_file = [
"""
    {
      "parent": "minecraft:item/generated",
      "textures": {
        "layer0": "anthemdiscs:item/music_disc_{name}"
      }
    }

""",

"""
    {
      "comparator_output": 5,
      "description": {
        "translate": "item.anthemdiscs.music_disc_{name}.desc"
      },
      "length_in_seconds": {length_in_seconds_float},
      "sound_event": "anthemdiscs:{name}"
    }
    
""",
]