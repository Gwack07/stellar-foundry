package dev.stellarfoundry.core;

import com.mojang.logging.LogUtils;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import org.slf4j.Logger;

/**
 * Stellar Foundry Core - Java-side features for the Stellar Foundry pack.
 *
 * Use this mod for things KubeJS can't do well: blocks with block entities and custom
 * behaviour, rendering, performance-critical systems, deep hooks into Create, Northstar or
 * Aeronautics. Keep pack balance (recipes, quests) in KubeJS/datapacks where it is easy to tune.
 */
@Mod(StellarCore.MOD_ID)
public final class StellarCore {
    public static final String MOD_ID = "stellarcore";
    public static final Logger LOGGER = LogUtils.getLogger();

    public StellarCore(IEventBus modBus) {
        LOGGER.info("Stellar Foundry Core loaded");
    }
}
