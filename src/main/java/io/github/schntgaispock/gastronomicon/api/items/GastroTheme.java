package io.github.schntgaispock.gastronomicon.api.items;

import io.github.schntgaispock.gastronomicon.util.StringUtil;
import lombok.Getter;

public enum GastroTheme {
    WORKSTATION_TOOL("#ffffff"),
    TOOL("#55ffff"),
    INGREDIENT("#ffff55"),
    MECHANICAL("#00aaaa"),
    ELECTRIC("#aaaaff"),
    TRAP("#f4a51d"),
    REGULAR_FOOD("#1d90f4"),
    PERFECT_FOOD("#c91df4");

    private final @Getter String color;
    private final @Getter String loreColor;

    GastroTheme(String color, String loreColor) {
        this.color = StringUtil.hexColor(color);
        this.loreColor = StringUtil.hexColor(loreColor);
    }

    GastroTheme(String color) {
        this(color, "#aaaaaa");
    }
}