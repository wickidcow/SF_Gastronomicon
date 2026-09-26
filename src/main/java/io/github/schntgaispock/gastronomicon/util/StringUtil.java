package io.github.schntgaispock.gastronomicon.util;

import javax.annotation.Nonnull;

import lombok.experimental.UtilityClass;

@UtilityClass
public class StringUtil {

    private static final char LEGACY_COLOR_CHAR = '\u00A7';
    private static final String LEGACY_COLOR_CODES = "0123456789AaBbCcDdEeFfKkLlMmNnOoRrXx";

    @Nonnull
    public static String formatColors(String str) {
        char[] chars = str.toCharArray();
        for (int i = 0; i < chars.length - 1; i++) {
            if (chars[i] == '&' && LEGACY_COLOR_CODES.indexOf(chars[i + 1]) >= 0) {
                chars[i] = LEGACY_COLOR_CHAR;
                chars[i + 1] = Character.toLowerCase(chars[i + 1]);
            }
        }
        return new String(chars);
    }

    @Nonnull
    public static String hexColor(String hex) {
        if (hex == null || !hex.matches("#[0-9a-fA-F]{6}")) {
            throw new IllegalArgumentException("Expected a six-digit hex color");
        }

        StringBuilder result = new StringBuilder(14).append(LEGACY_COLOR_CHAR).append('x');
        for (int i = 1; i < hex.length(); i++) {
            result.append(LEGACY_COLOR_CHAR).append(Character.toLowerCase(hex.charAt(i)));
        }
        return result.toString();
    }

    public static String waterUsed(int mB, String suffix) {
        return "&8⇨ &9🪣 &7" + mB + " mB" + suffix;
    }

    public static String kebabCase(String str) {
        return str.replace("_", "-").replace(" ", "-").toLowerCase();
    }

}
