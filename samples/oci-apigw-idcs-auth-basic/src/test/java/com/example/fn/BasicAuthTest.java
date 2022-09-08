package com.example.fn;

import com.example.fn.util.ResourceServerConfig;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fnproject.fn.testing.*;
import org.junit.*;

import static org.junit.Assert.*;

import java.io.IOException;

public class BasicAuthTest {

    // set these variables with the test env values
    private static final String TEST_IDCS_URL = "";
    private static final String TEST_CLIENT_ID = "";
    private static final String TEST_CLIENT_SECRET = "";
    private static final String TEST_SCOPE_AUD = "";
    private static final String TEST_TOKEN = "";

    private static String INPUT_FORMAT = "{\n" +
            "  \"type\":\"TOKEN\",\n" +
            "  \"token\": \"Basic %s\"\n" +
            "}";
    private static String INVALID_TOKEN = "Basic ";

    private static final ObjectMapper mapper = new ObjectMapper();

    public static class Result {

        public boolean active;
        public String principal;
        public String[] scope;
        public String expiresAt;
    }

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
        testing.setConfig(ResourceServerConfig.CONFIG_KEY_CLIENT_ID, TEST_CLIENT_ID);
        testing.setConfig(ResourceServerConfig.CONFIG_KEY_CLIENT_SECRET, TEST_CLIENT_SECRET);
        testing.setConfig(ResourceServerConfig.CONFIG_KEY_IDCS_URL, TEST_IDCS_URL);
        testing.setConfig(ResourceServerConfig.CONFIG_KEY_SCOPE_AUD, TEST_SCOPE_AUD);

        final String input = String.format(INPUT_FORMAT, TEST_TOKEN);

        try {
            testing.givenEvent().withBody(input).enqueue();
            testing.thenRun(BasicAuth.class, "handleRequest");

            FnResult fnResult = testing.getOnlyResult();

            Result result = mapper.readValue(fnResult.getBodyAsString(), Result.class);
            assertTrue(result.active);
            System.out.println(fnResult.getBodyAsString());
        } finally {
            // do nothing
        }
    }
}