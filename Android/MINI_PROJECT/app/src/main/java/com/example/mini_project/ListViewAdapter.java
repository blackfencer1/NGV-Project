package com.example.mini_project;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

public class ListViewAdapter extends BaseAdapter {

    List<ListViewItem> listViewItemList;
    Context context_;

    public ListViewAdapter(List list, Context context) {
        listViewItemList = list;
        context_ = context;
    }

    @Override
    public int getCount() {
        return listViewItemList.size();
    }


    @Override
    public long getItemId(int position) {
        return position;
    }


    @Override
    public Object getItem(int position) {
        return listViewItemList.get(position);
    }

    // position에 위치한 데이터를 화면에 출력하는데 사용될 View를 리턴
    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        final Context context = parent.getContext();

        if (convertView == null) {
            LayoutInflater inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            convertView = inflater.inflate(R.layout.listview_item, parent, false);
        }

        ImageView iconImageView = (ImageView) convertView.findViewById(R.id.imageView_item);
        TextView titleTextView = (TextView) convertView.findViewById(R.id.textView_item1);
        TextView descTextView = (TextView) convertView.findViewById(R.id.textView_item2);

        // position에 위치한 데이터
        final ListViewItem listViewItem = listViewItemList.get(position);

        iconImageView.setImageURI(Uri.parse(listViewItem.getPath()));
        titleTextView.setText(listViewItem.getTitle());
        descTextView.setText(listViewItem.getContent());

        final ListViewItem item = (ListViewItem) getItem(position);

        // 리스트뷰 아이템중 한가지를 선택하면 상세화면으로 이동
        convertView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(context, DetailPage.class);
                intent.putExtra("ITEM", item);
                context.startActivity(intent);
            }
        });

        return convertView;
    }
}
