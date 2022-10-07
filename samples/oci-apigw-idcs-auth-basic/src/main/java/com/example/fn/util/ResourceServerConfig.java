package com.example.fn.util;

/**
 * Util class that contains the constants used across the function
 */
public final class ResourceServerConfig {

    private ResourceServerConfig() {
        //
    }

    public static final String TOKEN_PREFIX = "Basic ";

    public static final String CONFIG_KEY_IDCS_URL = "IDCS_URL";
    public static final String CONFIG_KEY_CLIENT_ID = "CLIENT_ID";
    public static final String CONFIG_KEY_CLIENT_SECRET = "CLIENT_SECRET";
    public static final String CONFIG_KEY_SCOPE_AUD = "SCOPE_AUD";

    public static final String DEFAULT_GRANT_TYPE = "password";

    public static final String HEADER_NAME_CONTENT_TYPE = "Content-Type";
    public static final String HEADER_NAME_AUTHORIZATION = "Authorization";
    public static final String HEADER_VALUE_CONTENT_TYPE = "application/x-www-form-urlencoded";

    public static final Integer HTTP_RESPONSE_OK = 200;

    public static final String TOKEN_CLAIM_KEY_EXPIRY = "exp";
    public static final String TOKEN_CLAIM_KEY_SUBJECT = "sub";
    public static final String TOKEN_CLAIM_KEY_SCOPE = "scope";
}