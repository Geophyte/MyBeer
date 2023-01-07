import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;

import javax.imageio.ImageIO;
import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonReader;
import javax.swing.*;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.io.InputStream;
import java.io.StringReader;
import java.io.UnsupportedEncodingException;
import java.util.List;

public class Backend {
    public static final String signupURL = "http://127.0.0.1:8000/api/v1/auth/register";
    public static final String loginURL = "http://127.0.0.1:8000/api/v1/auth/login";
    public static final String logoutURL = "http://127.0.0.1:8000/api/v1/auth/logout";
    public static final String userURL = "http://127.0.0.1:8000/api/v1/auth/user";
    public static final String dataURL = "http://127.0.0.1:8000/api/v1/";
    private static CloseableHttpClient client = HttpClients.createDefault();

    public static synchronized String getJsonString(String url, String token) {
        HttpGet request = new HttpGet(url);
        if(token != null) {
            request.setHeader("Authorization", "Token " + token);
        }

        try(CloseableHttpResponse response = client.execute(request)) {
            if(isResponseSuccessful(response)) {
                return EntityUtils.toString(response.getEntity());
            }
        } catch (ClientProtocolException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        return null;
    }

    public static synchronized BufferedImage getImage(String url) {
        HttpGet request = new HttpGet(url);
        try(CloseableHttpResponse response = client.execute(request);) {
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

    public static synchronized String post(String url, List<NameValuePair> params) {
        HttpPost request = new HttpPost(url);
        try {
            request.setEntity(new UrlEncodedFormEntity(params));
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

    public static synchronized String post(String url, String json, String token) {
        HttpPost request = new HttpPost(url);
        try {
            request.setEntity(new StringEntity(json));
            request.setHeader("Content-Type", "application/json");
            request.setHeader("Authorization", "Token " + token);

            CloseableHttpResponse response = client.execute(request);
            System.out.println(request);
            System.out.println(response);
            System.out.println(json);
            if(isResponseSuccessful(response)) {
                String stringResponse = EntityUtils.toString(response.getEntity());
                System.out.println(stringResponse);
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

    private static boolean isResponseSuccessful(HttpResponse response) {
        int statusCode = response.getStatusLine().getStatusCode();
        return statusCode >= 200 && statusCode < 300;
    }
}
