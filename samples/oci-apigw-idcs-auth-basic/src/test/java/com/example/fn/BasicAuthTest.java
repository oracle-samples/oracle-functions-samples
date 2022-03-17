package com.example.fn;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fnproject.fn.testing.*;
import org.junit.*;

import static org.junit.Assert.*;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Base64;

public class BasicAuthTest {

    private static final ObjectMapper mapper = new ObjectMapper();
    public static class Result {
       
        public boolean active;
        public String principal;
        public String[] scope;
        public String expiresAt;
    }
    private static final String IDCS_URL = ResourceServerConfig.IDCS_URL;
    private static String INPUT_FORMAT = "{\n" +
        "  \"type\":\"TOKEN\",\n" +
        "  \"token\": \"Basic %s\"\n" +
        "}";
    private static String INVALID_TOKEN = "Basic ";

    @Rule
    public final FnTestingRule testing = FnTestingRule.createDefault();

    @Test
    public void shouldReturnInactive() throws IOException {
        final String input = "{\n" +
            "  \"type\":\"TOKEN\",\n" +
            "  \"token\": \"" + INVALID_TOKEN + "\"\n" +
            "}";

            testing.givenEvent().withBody(input).enqueue();
            testing.thenRun(BasicAuth.class, "handleRequest");

            FnResult fnResult = testing.getOnlyResult();

            Result result = mapper.readValue(fnResult.getBodyAsString(), Result.class);
            assertFalse(result.active);
    }

    @Test
    public void shouldReturnActive() throws Exception {

        String token = ResourceServerConfig.TOKEN;

        final String input = String.format(INPUT_FORMAT, token);
        String[] user = new String(Base64.getDecoder().decode(token)).split(":", 2);
        String username = user[0];
        String password = user[1];
        String clientId = ResourceServerConfig.CLIENT_ID;
        String clientSecret = ResourceServerConfig.CLIENT_SECRET;
        String authzHdrVal = clientId + ":" + clientSecret;
        String idcsScope = ResourceServerConfig.SCOPE_AUD;

        String reqBody =   "grant_type=password" +
                "&username=" + username +
                "&password=" + password +
                "&scope=" + idcsScope;

        try {
            HttpClient client = HttpClient.newHttpClient();

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(IDCS_URL))
                    .header("Content-Type", "application/x-www-form-urlencoded")
                    .header("Authorization", "Basic " + Base64.getEncoder().encodeToString(authzHdrVal.getBytes("UTF-8")))
                    .POST(HttpRequest.BodyPublishers.ofString(reqBody))
                    .build();

            HttpResponse<String> response = client.send(    request,
                    HttpResponse.BodyHandlers.ofString() );
            System.out.println(response.statusCode());        

        testing.givenEvent().withBody(input).enqueue();
        testing.thenRun(BasicAuth.class, "handleRequest");            

        FnResult fnResult = testing.getOnlyResult();

        Result result = mapper.readValue(fnResult.getBodyAsString(), Result.class);
        assertTrue(result.active);
        System.out.println(fnResult.getBodyAsString());
        }
        finally{}
    }

}