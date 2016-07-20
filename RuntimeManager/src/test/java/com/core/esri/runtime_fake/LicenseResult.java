package com.core.esri.runtime_fake;

public enum LicenseResult {
    INVALID,
    EXPIRED,
    LOGIN_REQUIRED,
    VALID;

    private LicenseResult() {
    }

    static LicenseResult a(int var0) {
        return VALID;
    }
}