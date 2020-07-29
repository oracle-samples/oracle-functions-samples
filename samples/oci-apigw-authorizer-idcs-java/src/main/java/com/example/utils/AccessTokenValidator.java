/*
# oci-apigw-authorizer-idcs-java version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
*/

package com.example.utils;

import com.nimbusds.jose.JOSEException;
import com.nimbusds.jose.JWSAlgorithm;
import com.nimbusds.jose.jwk.JWKSet;
import com.nimbusds.jose.jwk.source.ImmutableJWKSet;
import com.nimbusds.jose.jwk.source.JWKSource;
import com.nimbusds.jose.proc.BadJOSEException;
import com.nimbusds.jose.proc.JWSKeySelector;
import com.nimbusds.jose.proc.JWSVerificationKeySelector;
import com.nimbusds.jose.proc.SecurityContext;
import com.nimbusds.jwt.JWTClaimsSet;
import com.nimbusds.jwt.proc.BadJWTException;
import com.nimbusds.jwt.proc.ConfigurableJWTProcessor;
import com.nimbusds.jwt.proc.DefaultJWTProcessor;

import java.io.CharArrayWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Validates access tokens
 */
public class AccessTokenValidator {

    private static JWKSet jwk;
    private static boolean isSafe = false;
    private static final ConfigurableJWTProcessor JWT_PROCESSOR = new DefaultJWTProcessor();
    private static JWKSource keySource;
    private static JWSKeySelector keySelector;

    public void init() {
        if(!AccessTokenValidator.isSafe) {
            try {
                jwk = JWKUtil.getJWK();
                keySource = new ImmutableJWKSet(jwk);
                keySelector = new JWSVerificationKeySelector(JWSAlgorithm.RS256, keySource);
                JWT_PROCESSOR.setJWSKeySelector(keySelector);
                AccessTokenValidator.isSafe = true;
                Logger.getLogger(AccessTokenValidator.class.getName()).log(Level.INFO, "Signing Key from IDCS successfully loaded!");
            } catch (Exception ex) {
                Logger.getLogger(AccessTokenValidator.class.getName()).log(Level.SEVERE, "Error loading Signing Key from IDCS", ex);
                AccessTokenValidator.isSafe = false;
            }
        }
    }

    //checks if the token is valid
    public JWTClaimsSet validate(String accessToken) {
        if(AccessTokenValidator.isSafe){

            try {
                SecurityContext ctx = null;
                JWTClaimsSet claimsSet = JWT_PROCESSOR.process(accessToken, ctx);

                //VALIDATE AUDIENCE
                if (claimsSet.getAudience().indexOf(ResourceServerConfig.SCOPE_AUD) >= 0) {
                    //CORRECT AUDIENCE
                    return claimsSet;
                } else {
                    throw new InvalidTokenException("Incorrect audience");
                }

            } catch (JOSEException ex) {
                ex.printStackTrace();
                //Logger.getLogger(AccessTokenValidator.class.getName()).log(Level.SEVERE, "System Exception validating the JWT signature", ex);
                //throw new ServletException(ex);
                throw new InvalidTokenException(ex.getMessage());
            } catch (BadJOSEException ex) {
                ex.printStackTrace();
                throw new InvalidTokenException(ex.getMessage());
                //BadJWEException, BadJWSException, BadJWTException
                //Bad JSON Web Encryption (JWE) exception. Used to indicate a JWE-protected object that couldn't be successfully decrypted or its integrity has been compromised.
                //Bad JSON Web Signature (JWS) exception. Used to indicate an invalid signature or hash-based message authentication code (HMAC).
                //Bad JSON Web Token (JWT) exception.
            } catch (ParseException ex) {
                ex.printStackTrace();
                throw new InvalidTokenException(ex.getMessage());
            }
        }else{
            throw new InvalidTokenException("Resource Server application is not able to validate tokens");
        }
    }
}
