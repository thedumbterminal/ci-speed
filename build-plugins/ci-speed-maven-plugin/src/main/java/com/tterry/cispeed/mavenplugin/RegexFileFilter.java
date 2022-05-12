package com.tterry.cispeed.mavenplugin;

import java.io.File;
import java.io.FileFilter;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class RegexFileFilter implements FileFilter {

    private Pattern pattern;

    public RegexFileFilter(String pattern){
        this.pattern = Pattern.compile(pattern);
    }

    @Override
    public boolean accept(File pathname) {
        Matcher matcher = pattern.matcher(pathname.getName());
        return matcher.matches();
    }
}
