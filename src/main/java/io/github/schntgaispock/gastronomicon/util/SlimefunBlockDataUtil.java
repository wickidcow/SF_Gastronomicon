package io.github.schntgaispock.gastronomicon.util;

import javax.annotation.Nullable;

import org.bukkit.Location;
import org.bukkit.block.Block;

import com.xzavier0722.mc.plugin.slimefun4.storage.controller.SlimefunBlockData;

import io.github.thebusybiscuit.slimefun4.api.items.SlimefunItem;
import io.github.thebusybiscuit.slimefun4.implementation.Slimefun;
import me.mrCookieSlime.Slimefun.api.inventory.BlockMenu;

/**
 * Access to Slimefun Legacy block data without the deprecated BlockStorage facade.
 *
 * <p>This intentionally mirrors the BlockStorage behaviors Gastronomicon used: reads synchronously
 * load block data before access, ID registration delegates to the current block-data controller,
 * custom values are updated on the loaded block record, and removal delegates to removeBlock.</p>
 */
public final class SlimefunBlockDataUtil {

    private SlimefunBlockDataUtil() {
    }

    @Nullable
    private static SlimefunBlockData getLoadedBlockData(Location location) {
        var controller = Slimefun.getDatabaseManager().getBlockDataController();
        var data = controller.getBlockData(location);

        if (data != null && !data.isDataLoaded()) {
            controller.loadBlockData(data);
        }

        return data;
    }

    public static void register(Block block, String itemId) {
        register(block.getLocation(), itemId);
    }

    public static void register(Location location, String itemId) {
        Slimefun.getDatabaseManager().getBlockDataController().createBlock(location, itemId);
    }

    public static void setData(Location location, String key, @Nullable String value) {
        if ("id".equals(key)) {
            if (value != null) {
                register(location, value);
            }
            return;
        }

        var data = getLoadedBlockData(location);
        if (data == null) {
            return;
        }

        if (value == null) {
            data.removeData(key);
        } else {
            data.setData(key, value);
        }
    }

    public static void remove(Block block) {
        remove(block.getLocation());
    }

    public static void remove(Location location) {
        Slimefun.getDatabaseManager().getBlockDataController().removeBlock(location);
    }

    @Nullable
    public static SlimefunItem getItem(Block block) {
        return getItem(block.getLocation());
    }

    @Nullable
    public static SlimefunItem getItem(Location location) {
        var data = getLoadedBlockData(location);
        return data == null ? null : SlimefunItem.getById(data.getSfId());
    }

    @Nullable
    public static String getId(Location location) {
        var data = getLoadedBlockData(location);
        return data == null ? null : data.getSfId();
    }

    @Nullable
    public static String getData(Location location, String key) {
        var data = getLoadedBlockData(location);
        return data == null ? null : data.getData(key);
    }

    @Nullable
    public static BlockMenu getMenu(Block block) {
        return getMenu(block.getLocation());
    }

    @Nullable
    public static BlockMenu getMenu(Location location) {
        var data = getLoadedBlockData(location);
        return data == null ? null : data.getBlockMenu();
    }
}
