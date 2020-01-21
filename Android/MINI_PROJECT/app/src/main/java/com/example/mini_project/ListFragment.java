package com.example.mini_project;


import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ListView;

import com.google.android.gms.maps.model.LatLng;

import java.util.ArrayList;
import java.util.List;

/**
 * A simple {@link Fragment} subclass.
 */
public class ListFragment extends Fragment {

    static ListView listView;
    static ListViewAdapter adapter;
    static List itemlist;


    public static ListFragment newInstance() {
        return new ListFragment();
    }


    @Override
    public View onCreateView(final LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_list, null);
        listView = (ListView) view.findViewById(R.id.listView);

        if (MainActivity.dbHelper == null) {
            MainActivity.dbHelper = new DBHelper(getActivity());
        }

        itemlist = MainActivity.dbHelper.getAllListViewItemData();
        adapter = new ListViewAdapter(itemlist, getContext());
        listView.setAdapter(adapter);
        adapter.notifyDataSetChanged();

        return view;
    }

}
