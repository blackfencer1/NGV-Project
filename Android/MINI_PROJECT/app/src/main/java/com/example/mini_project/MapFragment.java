package com.example.mini_project;


import android.app.Activity;
import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.net.Uri;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.design.widget.FloatingActionButton;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentActivity;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapView;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;


/**
 * A simple {@link Fragment} subclass.
 */
public class MapFragment extends Fragment implements OnMapReadyCallback {

    GoogleMap mMap;
    MapView mapView; // 플래그먼트에는 SupportManager보단 맵뷰가 더 간편함
    LatLng latLng;

    public static MapFragment newInstance() {
        return new MapFragment();
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_map, null);
        mapView = (MapView) view.findViewById(R.id.map_second);
        mapView.onCreate(savedInstanceState);
        mapView.onResume();
        mapView.getMapAsync(this);

        return view;
    }

    @Override
    public void onMapReady(GoogleMap googleMap) {

        mMap = googleMap;

        LatLng Seoul = new LatLng(35.176239, 128.646430);
        mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(Seoul,11));

        if(MainActivity.dbHelper == null){
            MainActivity.dbHelper = new DBHelper(getActivity());
        }

        final List<ListViewItem> itemList = MainActivity.dbHelper.getAllListViewItemData();
        for (int i = 0; i < itemList.size(); i++) {
            latLng = new LatLng(itemList.get(i).getLatitude(), itemList.get(i).getLongitude());
            mMap.addMarker(new MarkerOptions().position(latLng));
        }

        // 마커 클릭 이벤트 처리
        mMap.setOnMarkerClickListener(new GoogleMap.OnMarkerClickListener() {
            @Override
            public boolean onMarkerClick(final Marker marker) {
                Intent intent = new Intent(getActivity(), DetailPage.class);
                ListViewItem item = null;
                for(int i=0;i<itemList.size();i++){
                    if(marker.getPosition().latitude==itemList.get(i).getLatitude()
                            && marker.getPosition().longitude == itemList.get(i).getLongitude()) {
                        item = MainActivity.dbHelper.getItemById(itemList.get(i).get_id());
                        break;
                    }
                }
                intent.putExtra("ITEM", (Serializable) item);
                startActivity(intent);
                return false;
            }
        });

    }
}
