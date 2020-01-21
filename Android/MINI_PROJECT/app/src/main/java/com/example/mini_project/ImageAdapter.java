package com.example.mini_project;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.graphics.PorterDuff;
import android.graphics.drawable.ShapeDrawable;
import android.graphics.drawable.shapes.OvalShape;
import android.location.Address;
import android.location.Geocoder;
import android.net.Uri;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.GridView;
import android.widget.ImageView;
import android.widget.TextView;

import com.google.android.gms.maps.model.LatLng;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public class ImageAdapter extends BaseAdapter {
    List<ListViewItem> gridList;
    Context _context;

    public ImageAdapter(List<ListViewItem> gridList,Context _context) {
        this.gridList = gridList;
        this._context = _context;
    }

    @Override
    public int getCount() {
        return gridList.size();
    }

    @Override
    public Object getItem(int position) {
        return gridList.get(position);
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    public View getView(int position, View convertView, ViewGroup parent) {
        final Context context = parent.getContext();

        if (convertView == null) {
            LayoutInflater inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            convertView = inflater.inflate(R.layout.item_grid, parent, false);
        }

        ImageView imageView = (ImageView) convertView.findViewById(R.id.gridImage);
        TextView textView = (TextView) convertView.findViewById(R.id.gridText);

        ListViewItem listViewItem = gridList.get(position);
        imageView.setImageURI(Uri.parse(listViewItem.getPath()));
        textView.setText(listViewItem.getTitle());

        final ListViewItem item = (ListViewItem) getItem(position);
        return convertView;
    }
}