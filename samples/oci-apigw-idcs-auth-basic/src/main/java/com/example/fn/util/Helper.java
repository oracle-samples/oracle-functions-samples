package com.example.fn.util;

import static com.example.fn.util.ResourceServerConfig.TOKEN_PREFIX;
import static com.example.fn.util.ResourceServerConfig.HEADER_NAME_CONTENT_TYPE;
import static com.example.fn.util.ResourceServerConfig.HEADER_NAME_AUTHORIZATION;
import static com.example.fn.util.ResourceServerConfig.HEADER_VALUE_CONTENT_TYPE;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Base64;

import org.json.JSONObject;

/**
 * Util class that contains some common utility methods
 */
public final class Helper {

    private Helper() {
        //
    }

    /**
     * Creates the POST request body that will be sent to IDCS token endpoint
     * 
     * @param {@link String} username
     * @param {@link String} password
     * @param {@link String} scope
     * @param {@link String} grantType
     * @return {@link String} request body
     */
    public static String createRequestBody(final String username, final String password, final String scope,
            final String grantType) {
        return "grant_type=" + grantType +
                "&username=" + username +
                "&password=" + password +
                "&scope=" + scope;
    }

    /**
     * 
     * Calls IDCS token endpoint to validate the username and password and get the
     * access token.
     * 
     * @param {@link String} url
     * @param {@link String} authHeader
     * @param {@link String} requestBody
     * @return {@link HttpResponse}
     * @throws InterruptedException
     * @throws IOException
     */
    public static HttpResponse<String> callIDCS(final String url, final String authHeader, final String requestBody)
            throws IOException, InterruptedException {
        final HttpClient client = HttpClient.newHttpClient();

        final HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header(HEADER_NAME_CONTENT_TYPE, HEADER_VALUE_CONTENT_TYPE)
                .header(HEADER_NAME_AUTHORIZATION,
                        TOKEN_PREFIX + Base64.getEncoder().encodeToString(authHeader.getBytes("UTF-8")))
                .POST(HttpRequest.BodyPublishers.ofString(requestBody))
                .build();

        return client.send(request,
                HttpResponse.BodyHandlers.ofString());
    }

    /**
     * Returns the body from the access token. The token is of the JWT format with 3
     * parts separated by "." First part is header, body is the second part and the
     * last part is signature
     * 
     * @param response
     * @return
     */
    public static JSONObject getTokenBody(final String response) {
        final String[] chunks = response.split("\\.");
        final String respjson = new String(Base64.getUrlDecoder().decode(chunks[1]));
        return new JSONObject(respjson);
    }
}