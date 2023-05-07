package com.tterry.cispeed.mavenplugin;

import org.apache.hc.client5.http.classic.methods.HttpPost;
import org.apache.hc.client5.http.entity.UrlEncodedFormEntity;
import org.apache.hc.client5.http.entity.mime.FileBody;
import org.apache.hc.client5.http.entity.mime.MultipartEntityBuilder;
import org.apache.hc.client5.http.entity.mime.StringBody;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.CloseableHttpResponse;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.core5.http.ContentType;
import org.apache.hc.core5.http.HttpEntity;
import org.apache.hc.core5.http.NameValuePair;
import org.apache.hc.core5.http.io.entity.EntityUtils;
import org.apache.hc.core5.http.message.BasicNameValuePair;
import org.apache.maven.plugin.AbstractMojo;
import org.apache.maven.plugin.MojoExecutionException;
import org.apache.maven.plugin.MojoFailureException;
import org.apache.maven.plugins.annotations.LifecyclePhase;
import org.apache.maven.plugins.annotations.Mojo;
import org.apache.maven.plugins.annotations.Parameter;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;


@Mojo(name = "ci-speed", defaultPhase = LifecyclePhase.TEST)
public class CiSpeedMojo extends AbstractMojo {

    private final String CI_SPEED_BASE_URL = "https://ci-speed.herokuapp.com/api";

    @Parameter(property = "apiKey")
    String apiKey;

    @Parameter(property = "projectName")
    String projectName;

    @Parameter(property = "buildId")
    String buildId;

    @Parameter(property = "testReportDir")
    File testReportDir = new File("target/surefire-reports");

    @Parameter(property = "filterPattern")
    String filterPattern = ".+\\.xml";

    public CiSpeedMojo(){

    }
    public CiSpeedMojo(String apiKey, String projectName, String buildId, File testReportDir, String filterPattern){
        this.apiKey = apiKey;
        this.projectName = projectName;
        this.buildId = buildId;
        this.testReportDir = testReportDir;
        this.filterPattern = filterPattern;
    }

    private File[] reportFiles(File dir){
        return dir.listFiles(new RegexFileFilter(filterPattern));
    }

    private void executePost(String apiKey, String url, HttpEntity httpEntity) throws IOException{
        HttpPost httpPost = new HttpPost(url);
        httpPost.setEntity(httpEntity);
        httpPost.setHeader("Authentication-Token", apiKey);
        httpPost.setHeader("Accept", "application/json");
        getLog().info("executing request " + httpPost);
        try (final CloseableHttpClient httpclient = HttpClients.createDefault()) {
            try (final CloseableHttpResponse response = httpclient.execute(httpPost)) {
                getLog().info("----------------------------------------");
                getLog().info(response.toString());
                final HttpEntity resEntity = response.getEntity();
                if (resEntity != null) {
                    getLog().info("Response content length: " + resEntity.getContentLength());
                }
                EntityUtils.consume(resEntity);
            }
        }
    }

    private void uploadFile(String apiKey, String projectName, String buildId,File f) throws IOException {
        getLog().info("Uploading "+f.getAbsolutePath()+" ...");
        String uploadUrl = CI_SPEED_BASE_URL + "/test_runs/";

        final FileBody bin = new FileBody(f);
        final StringBody projectNamePart = new StringBody(projectName, ContentType.TEXT_PLAIN);
        final StringBody buildRefPart = new StringBody(buildId, ContentType.TEXT_PLAIN);

        final HttpEntity reqEntity = MultipartEntityBuilder.create()
                .addPart("file", bin)
                .addPart("project_name",projectNamePart)
                .addPart("build_ref", buildRefPart)
                .build();

        executePost(apiKey, uploadUrl, reqEntity);
    }

    private void createBuild(String apiKey, String projectName, String buildId) throws IOException {
        getLog().info(String.format("Creating build %s for project %s ...", buildId, projectName));
        String uploadUrl = CI_SPEED_BASE_URL + "/builds/";
        List<NameValuePair> nvps = new ArrayList<>();
        nvps.add(new BasicNameValuePair("project_name", projectName));
        nvps.add(new BasicNameValuePair("ref", buildId));
        executePost(apiKey, uploadUrl, new UrlEncodedFormEntity(nvps));
    }

    @Override
    public void execute() throws MojoExecutionException, MojoFailureException {
       getLog().info("Plugin running...");
        File[] files = reportFiles(testReportDir);
        if(files == null){
            getLog().info("No files found");
        } else {
            getLog().info(files.length + " Files found..");
            try {
                if (buildId == null || "".equals(buildId)) {
                    buildId = UUID.randomUUID().toString();
                }
                createBuild(apiKey, projectName, buildId);
                for (File f : files) {
                    uploadFile(apiKey, projectName, buildId, f);
                }
            } catch (IOException ioe) {
                throw new MojoFailureException("Unable to upload files", ioe);
            }
        }
    }
}