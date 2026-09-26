package io.github.schntgaispock.gastronomicon.util;

import javax.annotation.Nullable;

import org.bukkit.Location;
import org.bukkit.block.Block;

import com.xzavier0722.mc.plugin.slimefun4.storage.controller.SlimefunBlockData;

import io.github.thebusybiscuit.slimefun4.api.items.SlimefunItem;
import io.github.thebusybiscuit.slimefun4.implementation.Slimefun;
import me.mrCookieSlime.Slimefun.api.inventory.BlockMenu;

/**
 * Read-only access to Slimefun Legacy block data without the deprecated BlockStorage facade.
 *
 * <p>This intentionally mirrors BlockStorage's synchronous read behavior: block data is resolved
 * through the current controller and fully loaded before IDs, custom data, or menus are returned.</p>
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
