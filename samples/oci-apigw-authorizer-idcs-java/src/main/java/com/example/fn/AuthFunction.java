/*
# oci-apigw-authorizer-idcs-java version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
*/

package com.example.fn;

import com.example.utils.AccessTokenValidator;
import com.example.utils.InvalidTokenException;
import com.nimbusds.jwt.JWTClaimsSet;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

public class AuthFunction {

    private static final DateTimeFormatter ISO8601 = DateTimeFormatter.ISO_DATE_TIME;
    private static final String TOKEN_BEARER_PREFIX = "Bearer ";

    public static class Input {
        public String type;
        public String token;
    }

    public static class Result {
        // required
        public boolean active = false;
        public String principal;
        public String[] scope;
        public String expiresAt;

        // optional
        public String wwwAuthenticate;

        // optional
        public String clientId;

        // optional context
        public Map<String, Object> context;
    }

    public Result handleRequest(Input input) {
        System.out.println("oci-apigw-authorizer-idcs-java START");
        Result result = new Result();

        if (input.token == null || !input.token.startsWith(TOKEN_BEARER_PREFIX)) {
            result.active = false;
            result.wwwAuthenticate = "Bearer error=\"missing_token\"";
            System.out.println("oci-apigw-authorizer-idcs-java END (Token)");
            return result;
        }

        // remove "Bearer " prefix in the token string before processing
        String token = input.token.substring(TOKEN_BEARER_PREFIX.length());

        AccessTokenValidator accessTokenValidator = new AccessTokenValidator();
        accessTokenValidator.init();

        try {
            JWTClaimsSet claimsSet = accessTokenValidator.validate(token);

            // Now that we can trust the contents of the JWT we can build the APIGW auth result
            result.active = true;

            result.principal = claimsSet.getSubject();
            result.scope = claimsSet.getStringClaim("scope").split(" ");
            result.expiresAt = ISO8601.format(claimsSet.getExpirationTime().toInstant().atOffset(ZoneOffset.UTC));

            Map<String, Object> context = new HashMap<>();
            context.put("tenant", claimsSet.getStringClaim("tenant"));
            result.context = context;

        } catch (InvalidTokenException e) {
            e.printStackTrace();

            result.active = false;
            result.wwwAuthenticate = "Bearer error=\"invalid_token\", error_description=\"" + e.getMessage() + "\"";
        } catch (ParseException ex) {
            ex.printStackTrace();

            result.active = false;
            result.wwwAuthenticate = "Bearer error=\"invalid_token_claim\", error_description=\"" + ex.getMessage() + "\"";
        }

        System.out.println("oci-apigw-authorizer-idcs-java END");

        return result;
    }

}