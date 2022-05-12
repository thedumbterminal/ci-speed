package com.tterry.cispeed.mavenplugin;

import org.apache.maven.plugin.AbstractMojo;
import org.apache.maven.plugin.MojoExecutionException;
import org.apache.maven.plugin.MojoFailureException;
import org.apache.maven.plugins.annotations.LifecyclePhase;
import org.apache.maven.plugins.annotations.Mojo;
import org.apache.maven.plugins.annotations.Parameter;

@Mojo(name = "ci-speed", defaultPhase = LifecyclePhase.COMPILE)
public class CiSpeedMojo extends AbstractMojo {

    private final String CI_SPEED_URL = "";

    @Parameter(property = "apiKey")
    String apiKey;

    @Parameter(property = "buildId")
    String buildId;

    @Override
    public void execute() throws MojoExecutionException, MojoFailureException {
        getLog().info("Plugin running...");
    }


}