# A flexible and fast Minecraft server software written completely in Python.
# Copyright (C) 2021 PyMine

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
            
from __future__ import annotations

import random
import struct
import uuid

import pymine.types.nbt as nbt


class Player:
    def __init__(self, entity_id: int, data: nbt.TAG) -> None:
        self.entity_id = entity_id
        self.data = data

        self.uuid = uuid.UUID(bytes=struct.pack(">iiii", *data["UUID"]))

        self.stream = None

        self.props = None  # textures from the mojang api
        self.username = None
        self.brand = None
        self.locale = None
        self.view_distance = None
        self.chat_mode = None
        self.chat_colors = None
        self.displayed_skin_parts = None
        self.main_hand = None

        self.teleport_id = None

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def get(self, key, default=None):
        try:
            return self.data[key]
        except KeyError:
            return default

    @property
    def x(self) -> float:
        return self.data["Pos"][0].data

    @property
    def y(self) -> float:
        return self.data["Pos"][1].data

    @property
    def z(self) -> float:
        return self.data["Pos"][2].data

    @property
    def pos(self) -> tuple:
        return tuple(t.data for t in self.data["Pos"])

    @property
    def rotation(self) -> tuple:
        return tuple(t.data for t in self.data["Rotation"])

    @classmethod
    def new(cls, entity_id: int, uuid_: uuid.UUID, spawn: tuple, dimension: str) -> Player:
        return cls(entity_id, cls.new_nbt(uuid_, spawn, dimension))

    @staticmethod
    def new_nbt(uuid_: uuid.UUID, spawn: tuple, dimension: str) -> nbt.TAG:
        return nbt.TAG_Compound(
            "",
            [
                nbt.TAG_List("Pos", [nbt.TAG_Double(None, 0), nbt.TAG_Double(None, 0), nbt.TAG_Double(None, 0)]),
                nbt.TAG_List("Motion", [nbt.TAG_Double(None, 0), nbt.TAG_Double(None, 0), nbt.TAG_Double(None, 0)]),
                nbt.TAG_List("Rotation", [nbt.TAG_Float(None, 0), nbt.TAG_Float(None, 0)]),
                nbt.TAG_Float("FallDistance", 0),
                nbt.TAG_Short("Fire", -20),
                nbt.TAG_Short("Air", 300),
                nbt.TAG_Byte("OnGround", 1),
                nbt.TAG_Byte("NoGravity", 0),
                nbt.TAG_Byte("Invulnerable", 0),
                nbt.TAG_Int("PortalCooldown", 0),
                nbt.TAG_Int_Array("UUID", struct.unpack(">iiii", uuid_.bytes)),
                nbt.TAG_String("CustomName", ""),
                nbt.TAG_Byte("CustomNameVisible", 0),
                nbt.TAG_Byte("Silent", 0),
                nbt.TAG_List("Passengers", []),
                nbt.TAG_Byte("Glowing", 0),
                nbt.TAG_List("Tags", []),
                nbt.TAG_Float("Health", 20),
                nbt.TAG_Float("AbsorptionAmount", 0),
                nbt.TAG_Short("HurtTime", 0),
                nbt.TAG_Int("HurtByTimestamp", 0),
                nbt.TAG_Short("DeathTime", 0),
                nbt.TAG_Byte("FallFlying", 0),
                # nbt.TAG_Int('SleepingX', 0),
                # nbt.TAG_Int('SleepingY', 0),
                # nbt.TAG_Int('SleepingZ', 0),
                nbt.TAG_Compound("Brain", [nbt.TAG_Compound("memories", [])]),
                nbt.TAG_List(
                    "ivaributes",
                    [
                        nbt.TAG_Compound(
                            None,
                            [
                                nbt.TAG_String("Name", "generic.max_health"),
                                nbt.TAG_Double("Base", 20),
                                nbt.TAG_List("Modifiers", []),
                            ],
                        ),
                        nbt.TAG_Compound(
                            None,
                            [
                                nbt.TAG_String("Name", "generic.follow_range"),
                                nbt.TAG_Double("Base", 32),
                                nbt.TAG_List("Modifiers", []),
                            ],
                        ),
                        nbt.TAG_Compound(
                            None,
                            [
                                nbt.TAG_String("Name", "generic.knockback_resistance"),
                                nbt.TAG_Double("Base", 0),
                                nbt.TAG_List("Modifiers", []),
                            ],
                        ),
                        nbt.TAG_Compound(
                            None,
                            [
                                nbt.TAG_String("Name", "generic.movement_speed"),
                                nbt.TAG_Double("Base", 1),
                                nbt.TAG_List("Modifiers", []),
                            ],
                        ),
                        nbt.TAG_Compound(
                            None,
                            [
                                nbt.TAG_String("Name", "generic.attack_damage"),
                                nbt.TAG_Double("Base", 2),
                                nbt.TAG_List("Modifiers", []),
                            ],
                        ),
                        nbt.TAG_Compound(
                            None,
                            [
                                nbt.TAG_String("Name", "generic.armor"),
                                nbt.TAG_Double("Base", 0),
                                nbt.TAG_List("Modifiers", []),
                            ],
                        ),
                        nbt.TAG_Compound(
                            None,
                            [
                                nbt.TAG_String("Name", "generic.armor_toughness"),
                                nbt.TAG_Double("Base", 0),
                                nbt.TAG_List("Modifiers", []),
                            ],
                        ),
                        nbt.TAG_Compound(
                            None,
                            [
                                nbt.TAG_String("Name", "generic.attack_knockback"),
                                nbt.TAG_Double("Base", 0),
                                nbt.TAG_List("Modifiers", []),
                            ],
                        ),
                        nbt.TAG_Compound(
                            None,
                            [
                                nbt.TAG_String("Name", "generic.attack_speed"),
                                nbt.TAG_Double("Base", 4),
                                nbt.TAG_List("Modifiers", []),
                            ],
                        ),
                        nbt.TAG_Compound(
                            None,
                            [nbt.TAG_String("Name", "generic.luck"), nbt.TAG_Double("Base", 0), nbt.TAG_List("Modifiers", [])],
                        ),
                    ],
                ),
                nbt.TAG_List("ActiveEffects", []),
                nbt.TAG_Int("DataVersion", 2586),
                nbt.TAG_Int("playerGameType", 0),
                nbt.TAG_Int("previousPlayerGameType", -1),
                nbt.TAG_Int("Score", 0),
                nbt.TAG_String("Dimension", dimension),
                nbt.TAG_Int("SelectedItemSlot", 0),
                nbt.TAG_Compound(
                    "SelectedItem",
                    [nbt.TAG_Byte("Count", 1), nbt.TAG_String("id", "minecraft:air"), nbt.TAG_Compound("tag", [])],
                ),
                nbt.TAG_String("SpawnDimension", "overworld"),
                nbt.TAG_Int("SpawnX", spawn[0]),
                nbt.TAG_Int("SpawnY", spawn[1]),
                nbt.TAG_Int("SpawnZ", spawn[2]),
                nbt.TAG_Byte("SpawnForced", 0),
                nbt.TAG_Int("foodLevel", 20),
                nbt.TAG_Float("foodExhaustionLevel", 0),
                nbt.TAG_Float("foodSaturationLevel", 5),
                nbt.TAG_Int("foodTickTimer", 0),
                nbt.TAG_Int("XpLevel", 0),
                nbt.TAG_Float("XpP", 0),
                nbt.TAG_Int("XpTotal", 0),
                nbt.TAG_Int("XpSeed", random.randint(-2147483648, 2147483647)),
                nbt.TAG_List("Inventory", []),
                nbt.TAG_List("EnderItems", []),
                nbt.TAG_Compound(
                    "abilities",
                    [
                        nbt.TAG_Float("walkSpeed", 0.1),
                        nbt.TAG_Float("flySpeed", 0.05),
                        nbt.TAG_Byte("mayfly", 0),
                        nbt.TAG_Byte("flying", 0),
                        nbt.TAG_Byte("invulnerable", 0),
                        nbt.TAG_Byte("mayBuild", 1),
                        nbt.TAG_Byte("instabuild", 0),
                    ],
                ),
                # nbt.TAG_Compound('enteredNetherPosition', [nbt.TAG_Double('x', 0), nbt.TAG_Double('y', 0), nbt.TAG_Double('z', 0)]),
                # nbt.TAG_Compound('RootVehicle', [
                #     nbt.TAG_Int_Array('Attach', [0, 0, 0, 0]),
                #     nbt.TAG_Compound('Entity', [])
                # ]),
                nbt.TAG_Byte("seenCredits", 0),
                nbt.TAG_Compound(
                    "recipeBook",
                    [
                        nbt.TAG_List("recipes", []),
                        nbt.TAG_List("toBeDisplayed", []),
                        nbt.TAG_Byte("isFilteringCraftable", 0),
                        nbt.TAG_Byte("isGuiOpen", 0),
                        nbt.TAG_Byte("isFurnaceFilteringCraftable", 0),
                        nbt.TAG_Byte("isFurnaceGuiOpen", 0),
                        nbt.TAG_Byte("isBlastingFurnaceFilteringCraftable", 0),
                        nbt.TAG_Byte("isBlastingFurnaceGuiOpen", 0),
                        nbt.TAG_Byte("isSmokerFilteringCraftable", 0),
                        nbt.TAG_Byte("isSmokerGuiOpen", 0),
                    ],
                ),
            ],
        )

    def __str__(self) -> str:
        return self.username
