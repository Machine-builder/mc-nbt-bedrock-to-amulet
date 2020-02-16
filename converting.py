'''

basically, I need to turn this :

TAG_Compound-:[TAG_Byte-Findable:0, TAG_List-Items:[TAG_Compound-0:
[TAG_Byte-Count:1, TAG_Short-Damage:0, TAG_String-Name:minecraft:stone_sword,
TAG_Byte-Slot:0, TAG_Compound-tag:[TAG_Int-Damage:0, TAG_List-ench:
[TAG_Compound-0:[TAG_Short-id:9, TAG_Short-lvl:2]]]]], TAG_String-id:Chest,
TAG_Byte-isMovable:1]

into this :

{Findable: 0b, Items: [{Count: 1b, Damage: 0s, Name: "minecraft:stone_sword",
Slot: 0b, tag: {ench: [{id: 9s, lvl: 2s}]}}], id: "Chest", isMovable: 1b,
x: 10, y: 4, z: 14}

{
    Findable: 0b,
    Items: [
        {
            Count: 1b,
            Damage: 0s,
            Name: "minecraft:stone_sword",
            Slot: 0b,
            tag: {
                ench: [
                    {
                        id: 9s,
                        lvl: 2s
                    }
                ]
            }
        }
    ],
    id: "Chest",
    isMovable: 1b
}

'''