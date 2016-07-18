package com.esri.core.runtime;

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
