package com.core.esri.runtime_fake;

public enum LicenseLevel {
    DEVELOPER,
    BASIC,
    STANDARD;

    private LicenseLevel() {
    }

    static LicenseLevel a(int var0) {
        return STANDARD;
    }
}
