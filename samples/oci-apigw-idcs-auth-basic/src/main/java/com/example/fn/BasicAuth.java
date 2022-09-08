package com.example.fn;

import static com.example.fn.util.ResourceServerConfig.TOKEN_PREFIX;
import static com.example.fn.util.ResourceServerConfig.CONFIG_KEY_IDCS_URL;
import static com.example.fn.util.ResourceServerConfig.CONFIG_KEY_CLIENT_ID;
import static com.example.fn.util.ResourceServerConfig.CONFIG_KEY_CLIENT_SECRET;
import static com.example.fn.util.ResourceServerConfig.CONFIG_KEY_SCOPE_AUD;
import static com.example.fn.util.ResourceServerConfig.DEFAULT_GRANT_TYPE;
import static com.example.fn.util.ResourceServerConfig.TOKEN_CLAIM_KEY_EXPIRY;
import static com.example.fn.util.ResourceServerConfig.TOKEN_CLAIM_KEY_SUBJECT;
import static com.example.fn.util.ResourceServerConfig.TOKEN_CLAIM_KEY_SCOPE;

import java.net.http.HttpResponse;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.lang.InterruptedException;
import org.json.JSONObject;

import com.example.fn.util.Helper;
import com.fnproject.fn.api.FnConfiguration;
import com.fnproject.fn.api.RuntimeContext;

import java.util.*;

/**
 * Main class implementing the {@code handleRequest} method, takes the user
 * credentials as input, authenticates the credentials against the identity
 * provider and if the authentication is successful then returns the following
 * claims from the access token <br/>
 * <ul>
 * <li>exp</li>
 * <li>sub</li>
 * <li>scope</li>
 * </ul>
 */
public class BasicAuth {

    private static String IDCS_URL = null;
    private static String CLIENT_ID = null;
    private static String CLIENT_SECRET = null;
    private static String SCOPE_AUD = null;

    /**
     * Reads the configuration parameters and sets the respective variables during
     * function initialization.
     * 
     * @param {@link RuntimeContext} ctx
     */
    @FnConfiguration
    public void config(final RuntimeContext ctx) {
        IDCS_URL = ctx.getConfigurationByKey(CONFIG_KEY_IDCS_URL).orElse(null);
        CLIENT_ID = ctx.getConfigurationByKey(CONFIG_KEY_CLIENT_ID).orElse(null);
        CLIENT_SECRET = ctx.getConfigurationByKey(CONFIG_KEY_CLIENT_SECRET).orElse(null);
        SCOPE_AUD = ctx.getConfigurationByKey(CONFIG_KEY_SCOPE_AUD).orElse(null);
    }

    /**
     * Entry point of the function
     * 
     * @param {@link Input} input
     * @return {@link Result}
     * @throws UnsupportedEncodingException
     * @throws InterruptedException
     */
    public Result handleRequest(final Input input) throws UnsupportedEncodingException, InterruptedException {
        final Result returnValue = new Result();

        if (!isConfigValid()) {
            returnValue.active = false;
            System.out.println(
                    "Function initialization error, all config parameters not set, please ensure that following config variables are set IDCS_URL, CLIENT_ID, CLIENT_SECRET");
            return returnValue;
        }

        if (input.token == null || !input.token.startsWith(TOKEN_PREFIX)) {
            returnValue.active = false;
            System.out.println("Request error, missing credentials");
            return returnValue;
        }

        final String[] user = getUserDetailsFromToken(input.token);
        if (user.length != 2 || user[0] == null || user[0].isEmpty() || user[1] == null || user[1].isEmpty()) {
            returnValue.active = false;
            System.out.println("Request error username or password missing");
            return returnValue;
        }

        final String authzHdrVal = CLIENT_ID + ":" + CLIENT_SECRET;
        final String reqBody = Helper.createRequestBody(user[0], user[1], SCOPE_AUD, DEFAULT_GRANT_TYPE);

        try {
            final HttpResponse<String> response = Helper.callIDCS(IDCS_URL, authzHdrVal, reqBody);

            if (response.statusCode() == 200) {
                final String responseString = (String) response.body();
                final JSONObject payload = Helper.getTokenBody(responseString);

                final Date expTime = new Date(payload.getLong(TOKEN_CLAIM_KEY_EXPIRY) * 1000);
                returnValue.principal = payload.getString(TOKEN_CLAIM_KEY_SUBJECT);
                returnValue.scope = payload.getString(TOKEN_CLAIM_KEY_SCOPE).split(" ");
                returnValue.expiresAt = expTime.toString();
                returnValue.active = true;

                System.out.println("Authentication successful");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return returnValue;
    }

    /**
     * Returns true if all the configuration variables are set else returns false
     * 
     * @return
     */
    private boolean isConfigValid() {
        if (IDCS_URL != null && !IDCS_URL.trim().isEmpty()
                && CLIENT_ID != null && !CLIENT_ID.trim().isEmpty()
                && CLIENT_SECRET != null && !CLIENT_SECRET.isEmpty()
                && SCOPE_AUD != null && !SCOPE_AUD.trim().isEmpty()) {
            return true;
        }
        return false;
    }

    /**
     * The input contains the username and password in {@link Base64} encoded
     * format. The format of the token is Base64 encoded <username>:<password>. This
     * function decodes the token and returns the username and password.
     * 
     * @param {@link String} token
     * @return {@link String} array with username and password
     */
    private String[] getUserDetailsFromToken(final String token) {
        final String data = token.substring(TOKEN_PREFIX.length());
        final String[] user = new String(Base64.getDecoder().decode(data)).split(":", 2);
        return user;
    }

    public static class Input {
        public String type;
        public String token;
    }

    public static class Result {
        public boolean active = false;
        public String principal;
        public String[] scope;
        public String expiresAt;
    }
}