package com.tterry.cispeed.mavenplugin;

import org.apache.hc.client5.http.classic.methods.HttpPost;
import org.apache.hc.client5.http.entity.mime.FileBody;
import org.apache.hc.client5.http.entity.mime.MultipartEntityBuilder;
import org.apache.hc.client5.http.entity.mime.StringBody;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.CloseableHttpResponse;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.core5.http.ContentType;
import org.apache.hc.core5.http.HttpEntity;
import org.apache.hc.core5.http.io.entity.EntityUtils;
import org.apache.maven.plugin.AbstractMojo;
import org.apache.maven.plugin.MojoExecutionException;
import org.apache.maven.plugin.MojoFailureException;
import org.apache.maven.plugins.annotations.LifecyclePhase;
import org.apache.maven.plugins.annotations.Mojo;
import org.apache.maven.plugins.annotations.Parameter;

import java.io.File;
import java.io.IOException;


@Mojo(name = "ci-speed", defaultPhase = LifecyclePhase.COMPILE)
public class CiSpeedMojo extends AbstractMojo {

    private final String CI_SPEED_BASE_URL = "https://ci-speed.herokuapp.com/";

    @Parameter(property = "apiKey")
    String apiKey;

    @Parameter(property = "buildId")
    String buildId;

    @Parameter(property = "testReportDir")
    File testReportDir;

    @Parameter(property = "filterPattern")
    String filterPattern;

    private File[] reportFiles(File dir){
        return dir.listFiles(new RegexFileFilter(filterPattern));
    }

    private void uploadFile(File f) throws IOException {
        getLog().info("Uploading "+f.getAbsolutePath()+" ...");
        String uploadUrl = CI_SPEED_BASE_URL + "/test_runs/";
        HttpPost httpPost = new HttpPost(uploadUrl);
        final FileBody bin = new FileBody(f);
        final StringBody comment = new StringBody("tim test", ContentType.TEXT_PLAIN);

        final HttpEntity reqEntity = MultipartEntityBuilder.create()
                .addPart("file", bin)
                .addPart("project_name", comment)
                .build();

        httpPost.setEntity(reqEntity);
        getLog().info("executing request " + httpPost);
        try (final CloseableHttpClient httpclient = HttpClients.createDefault()) {
            try (final CloseableHttpResponse response = httpclient.execute(httpPost)) {
                getLog().info("----------------------------------------");
                getLog().info(response.toString());
                final HttpEntity resEntity = response.getEntity();
                if (resEntity != null) {
                    System.out.println("Response content length: " + resEntity.getContentLength());
                }
                EntityUtils.consume(resEntity);
            }
        }
    }

    @Override
    public void execute() throws MojoExecutionException, MojoFailureException {
        getLog().info("Plugin running...");
        File[] files = reportFiles(testReportDir);
        getLog().info("Files found..");
        try {
            for (File f : files) {
                uploadFile(f);
            }
        }
        catch(IOException ioe){
            throw new MojoFailureException("Unable to upload files", ioe);
        }
    }


}