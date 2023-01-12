import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.mime.MultipartEntityBuilder;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ByteArrayEntity;
import org.apache.http.entity.StringEntity;
import org.apache.http.entity.mime.content.ContentBody;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;

import javax.imageio.ImageIO;
import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonReader;
import javax.swing.*;
import java.awt.image.BufferedImage;
import java.io.*;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.util.List;

/**
 * The Backend class contains public static final constants for URLs used to access the backend server,
 * as well as static methods for making HTTP requests to the server.
 * It is a utility class for making HTTP requests to the server, and does not have any non-static members.
 * The class also creates a default CloseableHttpClient object for use in making requests.
 *
 * @see #signupURL
 * @see #loginURL
 * @see #logoutURL
 * @see #userURL
 * @see #dataURL
 */
public class Backend {
    /**
     * The URL used to register a new user
     */
    public static final String signupURL = "http://127.0.0.1:8000/api/v1/auth/register";
    /**
     * The URL used to login
     */
    public static final String loginURL = "http://127.0.0.1:8000/api/v1/auth/login";
    /**
     * The URL used to logout
     */
    public static final String logoutURL = "http://127.0.0.1:8000/api/v1/auth/logout";
    /**
     * The URL used to get information about the logged in user
     */
    public static final String userURL = "http://127.0.0.1:8000/api/v1/auth/user";
    /**
     * The general URL for data requests that needs to be suffixed with for example "beers/" or "user/".
     */
    public static final String dataURL = "http://127.0.0.1:8000/api/v1/";
    private static CloseableHttpClient client = HttpClients.createDefault();

    /**
     * This method returns a JSON string from a given URL by making an HTTP GET request to the URL using the Apache HttpClient library.
     * The request includes an "Authorization" header with a "Token " + token value if a token is provided.
     * If the response is successful (determined by the isResponseSuccessful method), the JSON string is retrieved from the response's HttpEntity using the EntitiesUtils.toString method.
     * If an error occurs while making the request or reading the JSON string, a RuntimeException is thrown.
     *
     * @param url the URL of the JSON string to be retrieved
     * @param token an optional token to include in the "Authorization" header
     * @return the JSON string at the specified URL, or null if the response was not successful
     */
    public static synchronized String getJsonString(String url, String token) {
        HttpGet request = new HttpGet(url);
        if (token != null) {
            request.setHeader("Authorization", "Token " + token);
        }

        try (CloseableHttpResponse response = client.execute(request)) {
            if (isResponseSuccessful(response)) {
                return EntityUtils.toString(response.getEntity());
            }
        } catch (ClientProtocolException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        return null;
    }

    /**
     * This method returns a buffered image from a given URL by making an HTTP GET request to the URL using the Apache HttpClient library.
     * If the response is successful (determined by the isResponseSuccessful method), the image is read from the InputStream of the response's HttpEntity and returned as a BufferedImage.
     * If an error occurs while making the request or reading the image, a RuntimeException is thrown.
     *
     * @param url the URL of the image to be retrieved
     * @return the BufferedImage at the specified URL, or null if the response was not successful
     */
    public static synchronized BufferedImage getImage(String url) {
        HttpGet request = new HttpGet(url);

        try(CloseableHttpResponse response = client.execute(request)) {
            if(isResponseSuccessful(response)) {
                HttpEntity entity = response.getEntity();
                InputStream inputStream = entity.getContent();
                return ImageIO.read(inputStream);
            }
        } catch (ClientProtocolException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        return null;
    }

    /**
     * This method sends a HTTP POST request to a given URL using the Apache HttpClient library.
     * The request includes an "Authorization" header with a "Token " + token value and an empty ByteArrayEntity.
     * If the response is successful (determined by the isResponseSuccessful method), the method returns true.
     * If an error occurs while making the request, a RuntimeException is thrown.
     *
     * @param url the URL to send the POST request to
     * @param token the token to include in the "Authorization" header
     * @return true if the response is successful, false otherwise
     */
    public static synchronized boolean post(String url, String token) {
        HttpPost request = new HttpPost(url);
        try {
            request.setEntity(new ByteArrayEntity(new byte[0]));
            request.setHeader("Authorization", "Token " + token);

            CloseableHttpResponse response = client.execute(request);
            if(isResponseSuccessful(response)) {
                return true;
            }
        } catch (UnsupportedEncodingException e) {
            throw new RuntimeException(e);
        } catch (ClientProtocolException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        return false;
    }

    /**
     * This method sends a HTTP POST request to a given URL with a list of NameValuePairs as the body of the request, using the Apache HttpClient library.
     * If the response is successful (determined by the isResponseSuccessful method), the method return the response body as a string, using the EntitiesUtils.toString method.
     * If an error occurs while making the request, a RuntimeException is thrown.
     *
     * @param url the URL to send the POST request to
     * @param params a list of NameValuePairs to include in the body of the request
     * @return the response body as a string if the response is successful, null otherwise
     */
    public static synchronized String post(String url, List<NameValuePair> params) {
        HttpPost request = new HttpPost(url);
        try {
            request.setEntity(new UrlEncodedFormEntity(params, "UTF-8"));
            CloseableHttpResponse response = client.execute(request);
            if(isResponseSuccessful(response)) {
                return EntityUtils.toString(response.getEntity());
            }
        } catch (UnsupportedEncodingException e) {
            throw new RuntimeException(e);
        } catch (ClientProtocolException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        return null;
    }

    /**
     * This method sends a HTTP POST request to a given URL with a JSON string as the body of the request, using the Apache HttpClient library.
     * The body of the request is encoded as a StringEntity, using the UTF-8 character set. The request also includes "Content-Type" and "Authorization" headers.
     * If the response is successful (determined by the isResponseSuccessful method), the method return the response body as a string, using the EntitiesUtils.toString method.
     * If an error occurs while making the request, a RuntimeException is thrown.
     *
     * @param url the URL to send the POST request to
     * @param json a json string to include in the body of the request
     * @param token the token to include in the "Authorization" header
     * @return the response body as a string if the response is successful, null otherwise
     */
    public static synchronized String post(String url, String json, String token) {
        HttpPost request = new HttpPost(url);
        try {
            request.setEntity(new StringEntity(json, "UTF-8"));
            request.setHeader("Content-Type", "application/json; charset=UTF-8");
            request.setHeader("Authorization", "Token " + token);

            CloseableHttpResponse response = client.execute(request);
            if(isResponseSuccessful(response)) {
                String stringResponse = EntityUtils.toString(response.getEntity());
                return stringResponse;
            }
        } catch (UnsupportedEncodingException e) {
            throw new RuntimeException(e);
        } catch (ClientProtocolException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        return null;
    }

    /**
     * This method sends a HTTP POST request to a given URL with beer data and an image as the body of the request, using the Apache HttpClient library and the MultipartEntityBuilder.
     * The request includes "Authorization" header with a "Token " + token value.
     * The request body includes "name", "description", "category" as text fields and "image_url" as binary field.
     * If the response is successful (determined by the isResponseSuccessful method), the method return the response body as a string, using the EntitiesUtils.toString method.
     * If an error occurs while making the request, a RuntimeException is thrown.
     *
     * @param url the URL to send the POST request to
     * @param name the name of the beer
     * @param description the description of the beer
     * @param category the category id of the beer
     * @param image the image file of the beer
     * @param token the token to include in the "Authorization" header
     * @return the response body as a string if the response is successful, null otherwise
     */
    public static synchronized String postBeer(String url, String name, String description, int category, File image, String token) {
        HttpPost request = new HttpPost(url);
        request.setHeader("Authorization", "Token " + token);
        try {
            MultipartEntityBuilder builder = MultipartEntityBuilder.create();
            ContentType contentType = ContentType.create("text/plain", Charset.forName("UTF-8"));
            builder.addTextBody("name", name, contentType);
            builder.addTextBody("description", description, contentType);
            builder.addTextBody("category", "" + category, contentType);

            if(image != null) {
                builder.addBinaryBody("image_url", image);
            } else {
                builder.addBinaryBody("image_url", new byte[0]);
            }

            request.setEntity(builder.build());
            CloseableHttpResponse response = client.execute(request);
            if(isResponseSuccessful(response)) {
                return EntityUtils.toString(response.getEntity());
            }
        } catch (UnsupportedEncodingException e) {
            throw new RuntimeException(e);
        } catch (ClientProtocolException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        return null;
    }

    /**
     * This method checks whether a HTTP response is successful or not by checking the status code.
     * A response is considered successful if the status code is in the range of 200 and 299 (inclusive).
     *
     * @param response the HTTP response to check
     * @return true if the response is successful, false otherwise
     */
    private static boolean isResponseSuccessful(HttpResponse response) {
        int statusCode = response.getStatusLine().getStatusCode();
        return statusCode >= 200 && statusCode < 300;
    }
}
