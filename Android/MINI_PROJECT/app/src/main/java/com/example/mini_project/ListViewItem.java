package com.example.mini_project;

import android.graphics.Bitmap;
import android.graphics.drawable.Drawable;
import android.net.Uri;

import java.io.Serializable;

public class ListViewItem implements Serializable {
    private int id;
    private String path ;
    private String titleStr ;
    private String contStr ;
    private double latitude;
    private double longitude;

    public void set_id(int id){ this.id = id; }
    public void setPath(String path) {
        this.path = path ;
    }
    public void setTitle(String title) {
        titleStr = title ;
    }
    public void setContent(String content) {
        contStr = content ;
    }
    public void setLatitude(double lat){latitude=lat;}
    public void setLongitude(double log){longitude=log;}


    public int get_id(){ return this.id; }
    public String getPath() {
        return this.path ;
    }
    public String getTitle() {
        return this.titleStr ;
    }
    public String getContent() {
        return this.contStr ;
    }
    public double getLatitude(){return this.latitude;}
    public double getLongitude(){return this.longitude;}
}