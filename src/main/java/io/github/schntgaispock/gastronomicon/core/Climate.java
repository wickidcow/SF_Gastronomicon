package io.github.schntgaispock.gastronomicon.core;

import org.bukkit.Location;
import org.bukkit.Material;
import org.bukkit.block.Biome;
import org.bukkit.block.Block;
import org.bukkit.inventory.ItemStack;

import io.github.thebusybiscuit.slimefun4.libraries.dough.items.CustomItemStack;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
public enum Climate {
    DRY(new CustomItemStack(Material.SAND, "&eDry")),
    TEMPERATE(new CustomItemStack(Material.GRASS_BLOCK, "&eTemperate")),
    COLD(new CustomItemStack(Material.ICE, "&eCold")),
    SNOWY(new CustomItemStack(Material.SNOW, "&eSnowy")),
    NETHER(new CustomItemStack(Material.CRIMSON_NYLIUM, "&eNether")),
    END(new CustomItemStack(Material.END_STONE, "&eEnd"));

    private final @Getter ItemStack displayItem;

    public static Climate of(Biome biome) {
        return switch (biome.getKey().getKey()) {
            case "badlands", "wooded_badlands", "eroded_badlands", "desert",
                "savanna", "windswept_savanna", "savanna_plateau" -> DRY;
            case "deep_frozen_ocean", "old_growth_pine_taiga", "taiga",
                "old_growth_spruce_taiga", "windswept_hills", "windswept_forest",
                "windswept_gravelly_hills", "stony_shore" -> COLD;
            case "snowy_beach", "snowy_plains", "ice_spikes", "frozen_river",
                "frozen_ocean", "grove", "snowy_slopes", "snowy_taiga",
                "jagged_peaks", "frozen_peaks" -> SNOWY;
            case "nether_wastes", "crimson_forest", "warped_forest",
                "soul_sand_valley", "basalt_deltas" -> NETHER;
            case "the_end", "small_end_islands", "end_barrens", "end_midlands",
                "end_highlands", "the_void" -> END;
            default -> TEMPERATE;
        };
    }

    public static Climate of(Block block) {
        return of(block.getBiome());
    }

    public static Climate of(Location location) {
        return of(location.getBlock().getBiome());
    }
}
