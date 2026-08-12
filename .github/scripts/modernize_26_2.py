from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
VERSION = "1.1.4"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def replace_required(path: str, old: str, new: str, count: int = -1) -> None:
    text = read(path)
    if old not in text:
        raise RuntimeError(f"Expected text not found in {path}: {old[:120]!r}")
    write(path, text.replace(old, new, count))


# Build directly against the Albion Slimefun Legacy compatibility line.
write("pom.xml", f'''<project xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>
    <groupId>io.github.schntgaispock.gastronomicon</groupId>
    <artifactId>Gastronomicon</artifactId>
    <version>{VERSION}</version>

    <properties>
        <maven.compiler.release>21</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <paper.version>[26.2.build,26.3.build)</paper.version>
        <slimefun.legacy.version>Legacy-SNAPSHOT</slimefun.legacy.version>
    </properties>

    <repositories>
        <repository>
            <id>papermc</id>
            <url>https://repo.papermc.io/repository/maven-public/</url>
        </repository>
        <repository>
            <id>spigot-repo</id>
            <url>https://hub.spigotmc.org/nexus/content/repositories/snapshots/</url>
        </repository>
        <repository>
            <id>jitpack.io</id>
            <url>https://jitpack.io</url>
        </repository>
    </repositories>

    <build>
        <finalName>SF_Gastronomicon${{project.version}}</finalName>
        <defaultGoal>clean package</defaultGoal>
        <sourceDirectory>${{basedir}}/src/main/java</sourceDirectory>
        <resources>
            <resource>
                <directory>${{basedir}}/src/main/resources</directory>
                <filtering>true</filtering>
                <includes>
                    <include>*</include>
                    <include>schematics/*</include>
                </includes>
            </resource>
        </resources>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.14.1</version>
                <configuration>
                    <release>${{maven.compiler.release}}</release>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-shade-plugin</artifactId>
                <version>3.6.2</version>
                <configuration>
                    <minimizeJar>false</minimizeJar>
                    <createDependencyReducedPom>false</createDependencyReducedPom>
                    <relocations>
                        <relocation>
                            <pattern>io.github.mooy1.infinitylib</pattern>
                            <shadedPattern>io.github.schntgaispock.infinitylib</shadedPattern>
                        </relocation>
                        <relocation>
                            <pattern>org.bstats</pattern>
                            <shadedPattern>io.github.schntgaispock.bstats</shadedPattern>
                        </relocation>
                        <relocation>
                            <pattern>org.apache.commons.lang3</pattern>
                            <shadedPattern>io.github.schntgaispock.gastronomicon.libs.commons.lang3</shadedPattern>
                        </relocation>
                        <relocation>
                            <pattern>com.fasterxml.jackson</pattern>
                            <shadedPattern>io.github.schntgaispock.gastronomicon.libs.jackson</shadedPattern>
                        </relocation>
                    </relocations>
                    <filters>
                        <filter>
                            <artifact>*:*</artifact>
                            <excludes>
                                <exclude>META-INF/*.SF</exclude>
                                <exclude>META-INF/*.DSA</exclude>
                                <exclude>META-INF/*.RSA</exclude>
                            </excludes>
                        </filter>
                    </filters>
                </configuration>
                <executions>
                    <execution>
                        <phase>package</phase>
                        <goals><goal>shade</goal></goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>

    <dependencies>
        <dependency>
            <groupId>io.papermc.paper</groupId>
            <artifactId>paper-api</artifactId>
            <version>${{paper.version}}</version>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>com.github.slimefun</groupId>
            <artifactId>Slimefun</artifactId>
            <version>${{slimefun.legacy.version}}</version>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>com.github.schntgaispock</groupId>
            <artifactId>SlimeHUD</artifactId>
            <version>1.3.0</version>
            <scope>provided</scope>
            <exclusions>
                <exclusion><groupId>com.github.Slimefun</groupId><artifactId>Slimefun4</artifactId></exclusion>
            </exclusions>
        </dependency>
        <dependency>
            <groupId>io.github.mooy1</groupId>
            <artifactId>InfinityLib</artifactId>
            <version>1.3.9</version>
            <scope>compile</scope>
            <exclusions>
                <exclusion><groupId>com.github.Slimefun</groupId><artifactId>Slimefun4</artifactId></exclusion>
            </exclusions>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>1.18.46</version>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>com.google.code.findbugs</groupId>
            <artifactId>jsr305</artifactId>
            <version>3.0.2</version>
        </dependency>
        <dependency>
            <groupId>org.bstats</groupId>
            <artifactId>bstats-bukkit</artifactId>
            <version>3.2.1</version>
        </dependency>
        <dependency>
            <groupId>org.apache.commons</groupId>
            <artifactId>commons-lang3</artifactId>
            <version>3.20.0</version>
        </dependency>
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
            <version>2.22.0</version>
        </dependency>
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-annotations</artifactId>
            <version>2.22.0</version>
        </dependency>
    </dependencies>
</project>
''')

write("src/main/resources/plugin.yml", '''name: Gastronomicon
author: SchnTgaiSpock
description: A Slimefun addon that adds even more food to the game. Works best with ExoticGarden
main: io.github.schntgaispock.gastronomicon.Gastronomicon
website: https://github.com/wickidcow/SF_Gastronomicon
version: ${project.version}
api-version: '1.21'
depend:
  - Slimefun
softdepend:
  - SlimeHUD
  - ExoticGarden
  - DynaTech
loadbefore:
  - SlimeCustomizer
commands:
  gastronomicon:
    description: /gastronomicon
    aliases: [gastro, gn]
    usage: Press [tab] for usage hints
permissions:
  gastronomicon:
    checkprofile:
      description: Ability to view your Gastronomicon profile
      default: true
      op: true
    checkotherprofile:
      description: Ability to view another player's profile
      default: false
      op: true
    modifyprofile:
      description: Ability to change a player's Gastronomicon profile
      default: false
      op: false
''')

# Paper 1.21.11+/26.2 API compatibility from maintained forks.
for java in (ROOT / "src/main/java").rglob("*.java"):
    text = java.read_text(encoding="utf-8")
    text = text.replace("Attribute.GENERIC_MAX_HEALTH", "Attribute.MAX_HEALTH")
    text = text.replace("Enchantment.DURABILITY", "Enchantment.UNBREAKING")
    text = text.replace("Enchantment.LOOT_BONUS_BLOCKS", "Enchantment.FORTUNE")
    text = text.replace("Enchantment.LOOT_BONUS_MOBS", "Enchantment.LOOTING")
    text = re.sub(r"Material\.GRASS\b", "Material.SHORT_GRASS", text)
    text = text.replace("org.apache.commons.lang.Validate", "org.apache.commons.lang3.Validate")
    text = text.replace("org.apache.commons.lang.WordUtils", "org.apache.commons.lang3.text.WordUtils")
    java.write_text(text, encoding="utf-8")

write("src/main/java/io/github/schntgaispock/gastronomicon/core/Climate.java", '''package io.github.schntgaispock.gastronomicon.core;

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
''')

# PotionMeta modern API and duplicate-hand interaction hardening.
fermenter = "src/main/java/io/github/schntgaispock/gastronomicon/core/listeners/FermenterRefillListener.java"
replace_required(
    fermenter,
    "        if (e.getAction() != Action.RIGHT_CLICK_BLOCK || !e.getPlayer().isSneaking())\n            return;\n",
    "        if (e.getAction() != Action.RIGHT_CLICK_BLOCK || !e.getPlayer().isSneaking())\n            return;\n\n        // PlayerInteractEvent can fire once for each hand. Only consume/refill from the main hand.\n        if (e.getHand() != org.bukkit.inventory.EquipmentSlot.HAND)\n            return;\n",
    1,
)
replace_required(fermenter, ".getBasePotionData().getType()", ".getBasePotionType()")

gastro_stacks = "src/main/java/io/github/schntgaispock/gastronomicon/core/slimefun/GastroStacks.java"
text = read(gastro_stacks)
text = text.replace("import org.bukkit.potion.PotionData;\n", "")
text = text.replace(
    "        final PotionData data = new PotionData(PotionType.WATER);\n        meta.setBasePotionData(data);",
    "        meta.setBasePotionType(PotionType.WATER);",
)
text = re.sub(
    r"meta\.setBasePotionData\(new PotionData\(PotionType\.([A-Z0-9_]+)\)\);",
    r"meta.setBasePotionType(PotionType.\1);",
    text,
)
write(gastro_stacks, text)

# Biome is registry-backed on modern Paper and can no longer be switched as an enum.
item_setup = "src/main/java/io/github/schntgaispock/gastronomicon/core/setup/ItemSetup.java"
replace_required(
    item_setup,
    '''                return switch (l.getBlock().getBiome()) {
                    case RIVER, BEACH, OCEAN, COLD_OCEAN, DEEP_OCEAN, WARM_OCEAN, FROZEN_OCEAN, LUKEWARM_OCEAN, DEEP_COLD_OCEAN, DEEP_FROZEN_OCEAN, DEEP_LUKEWARM_OCEAN -> true;
                    default -> false;
                };''',
    '''                return switch (l.getBlock().getBiome().getKey().getKey()) {
                    case "river", "beach", "ocean", "cold_ocean", "deep_ocean", "warm_ocean",
                        "frozen_ocean", "lukewarm_ocean", "deep_cold_ocean", "deep_frozen_ocean",
                        "deep_lukewarm_ocean" -> true;
                    default -> false;
                };''',
    1,
)

# Fix an existing recursive display-name accessor exposed by modern code paths.
themed = "src/main/java/io/github/schntgaispock/gastronomicon/api/items/ThemedItemStack.java"
replace_required(themed, "        String name = getDisplayName();", "        String name = super.getDisplayName();", 1)

# Do not retain per-block workstation state after the block is destroyed.
workstation = "src/main/java/io/github/schntgaispock/gastronomicon/core/slimefun/items/workstations/manual/GastroWorkstation.java"
replace_required(
    workstation,
    "        menu.dropItems(l, getToolSlots());\n        menu.dropItems(l, getContainerSlots());",
    "        menu.dropItems(l, getToolSlots());\n        menu.dropItems(l, getContainerSlots());\n        lastInputHashAndRecipe.remove(l);",
    1,
)

# Make DynaTech integration optional and tolerant of either growth chamber being absent.
dynatech_path = "src/main/java/io/github/schntgaispock/gastronomicon/integration/DynaTechSetup.java"
old_dynatech = read(dynatech_path)
anchor = '        gc2 = SlimefunItem.getById("GROWTH_CHAMBER_MK2");\n'
if anchor not in old_dynatech:
    raise RuntimeError("Unable to locate DynaTech registration body")
body_start = old_dynatech.index(anchor) + len(anchor)
body_end = old_dynatech.rfind("\n    }\n\n}")
registration_body = old_dynatech[body_start:body_end].strip("\n")
write(dynatech_path, f'''package io.github.schntgaispock.gastronomicon.integration;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Arrays;

import org.bukkit.Material;
import org.bukkit.inventory.ItemStack;

import io.github.schntgaispock.gastronomicon.core.slimefun.GastroStacks;
import io.github.thebusybiscuit.slimefun4.api.items.SlimefunItem;
import lombok.Getter;

@Getter
public class DynaTechSetup {{

    private static SlimefunItem gc;
    private static SlimefunItem gc2;

    private static boolean register(SlimefunItem chamber, int seconds, ItemStack[] inputs, ItemStack[] outputs) {{
        if (chamber == null) return false;
        try {{
            final Method method = chamber.getClass().getMethod(
                "registerRecipe", int.class, ItemStack[].class, ItemStack[].class);
            method.invoke(chamber, seconds, inputs, outputs);
            return true;
        }} catch (NoSuchMethodException | IllegalAccessException | InvocationTargetException ignored) {{
            return false;
        }}
    }}

    private static boolean register(int seconds, ItemStack... outputs) {{
        if (outputs.length == 0) return false;
        final ItemStack[] inputs = {{ outputs[0].asOne() }};
        boolean registered = register(gc, seconds, inputs, outputs);
        final ItemStack[] mk2Outputs = Arrays.stream(outputs)
            .map(itemStack -> itemStack.asQuantity(itemStack.getAmount() * 3))
            .toArray(ItemStack[]::new);
        return register(gc2, seconds, inputs, mk2Outputs) || registered;
    }}

    public static boolean setup() {{
        gc = SlimefunItem.getById("GROWTH_CHAMBER");
        gc2 = SlimefunItem.getById("GROWTH_CHAMBER_MK2");
        if (gc == null && gc2 == null) return false;

{registration_body}
        return true;
    }}
}}
''')

gastronomicon = "src/main/java/io/github/schntgaispock/gastronomicon/Gastronomicon.java"
replace_required(
    gastronomicon,
    "                DynaTechSetup.setup();",
    "                if (!DynaTechSetup.setup()) {\n                    warn(\"DynaTech has no compatible Growth Chambers; crop automation integration was skipped.\");\n                }",
    1,
)
text = read(gastronomicon)
if "        getPlayerData().save();" in text:
    text = text.replace(
        "        getPlayerData().save();",
        "        if (playerData != null) {\n            playerData.save();\n        }",
        1,
    )
write(gastronomicon, text)

# Fail this migration if obsolete APIs survived the intended patch set.
obsolete = [
    "getBasePotionData()",
    "setBasePotionData(",
    "new PotionData(",
    "Attribute.GENERIC_MAX_HEALTH",
    "Enchantment.DURABILITY",
    "Enchantment.LOOT_BONUS_BLOCKS",
    "Enchantment.LOOT_BONUS_MOBS",
    "org.apache.commons.lang.Validate",
    "org.apache.commons.lang.WordUtils",
]
for java in (ROOT / "src/main/java").rglob("*.java"):
    data = java.read_text(encoding="utf-8")
    for token in obsolete:
        if token in data:
            raise RuntimeError(f"Obsolete API remained in {java.relative_to(ROOT)}: {token}")
    if re.search(r"Material\.GRASS\b", data):
        raise RuntimeError(f"Legacy Material.GRASS remained in {java.relative_to(ROOT)}")

# Replace the old Blob Builds workflow with a reproducible direct-JAR workflow.
old_workflow = ROOT / ".github/workflows/maven.yml"
if old_workflow.exists():
    old_workflow.unlink()

write(".github/workflows/build.yml", f'''name: Build direct Gastronomicon JAR

on:
  push:
    branches: [master]
  workflow_dispatch:

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Gastronomicon
        uses: actions/checkout@v4
        with:
          path: gastronomicon

      - name: Checkout Slimefun Legacy
        uses: actions/checkout@v4
        with:
          repository: wickidcow/Slimefun-Legacy
          ref: master
          path: slimefun-legacy

      - name: Set up Java 25
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '25'
          cache: maven

      - name: Publish Slimefun Legacy API to Maven local
        working-directory: slimefun-legacy
        run: |
          chmod +x gradlew
          ./gradlew publishToMavenLocal -PprojectVersion=Legacy-SNAPSHOT -x test --no-daemon

      - name: Build Gastronomicon for Paper 26.2
        working-directory: gastronomicon
        run: mvn -B -U clean package

      - name: Verify direct JAR
        working-directory: gastronomicon
        run: |
          test -f target/SF_Gastronomicon{VERSION}.jar
          jar tf target/SF_Gastronomicon{VERSION}.jar >/dev/null

      - name: Upload CI artifact (stored without recompression)
        uses: actions/upload-artifact@v4
        with:
          name: SF_Gastronomicon{VERSION}.jar
          path: gastronomicon/target/SF_Gastronomicon{VERSION}.jar
          compression-level: 0
          if-no-files-found: error

      - name: Publish direct unzipped JAR release asset
        working-directory: gastronomicon
        env:
          GH_TOKEN: ${{{{ github.token }}}}
        run: |
          TAG="v{VERSION}"
          JAR="target/SF_Gastronomicon{VERSION}.jar"
          if gh release view "$TAG" >/dev/null 2>&1; then
            gh release upload "$TAG" "$JAR" --clobber
          else
            gh release create "$TAG" "$JAR" --target "$GITHUB_SHA" \\
              --title "SF Gastronomicon {VERSION}" \\
              --notes "Paper 26.2 / Slimefun Legacy build. The attached SF_Gastronomicon{VERSION}.jar is the direct server JAR, not a ZIP archive."
          fi
''')

# The bootstrap migration files are intentionally one-shot.
for relative in [
    ".github/workflows/modernize-26-2.yml",
    ".github/modernize-26-2.pending",
    ".github/scripts/modernize_26_2.py",
]:
    p = ROOT / relative
    if p.exists():
        p.unlink()

print(f"Prepared SF_Gastronomicon {VERSION} for Paper 26.2 and Slimefun Legacy")
