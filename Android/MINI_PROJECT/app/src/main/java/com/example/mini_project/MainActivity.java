package com.example.mini_project;

import android.Manifest;
import android.content.ContentValues;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.res.AssetManager;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.location.Location;
import android.location.LocationManager;
import android.media.Image;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Handler;
import android.os.Looper;
import android.support.annotation.NonNull;
import android.support.design.widget.BottomNavigationView;
import android.support.design.widget.FloatingActionButton;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.FragmentTransaction;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.firebase.geofire.GeoFire;
import com.firebase.geofire.GeoLocation;
import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationCallback;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationResult;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.kakao.network.NetworkTask;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import github.vatsal.easyweather.retrofit.models.Main;
import jxl.Sheet;
import jxl.Workbook;

public class MainActivity extends AppCompatActivity {

    BottomNavigationView bottomNavigationView;
    FloatingActionButton fab;
    public static DBHelper dbHelper;
    public static SQLiteDatabase db;
    public static List<LatLng> placeList;
    private DatabaseReference myDetectionRef;
    boolean isDetect = false;

    private static final int REQUEST_CODE_LOCATION = 2;
    private LocationCallback locationCallback;
    private LocationRequest locationRequest;
    private Location currentLocation;
    private FusedLocationProviderClient fusedLocationProviderClient;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // 권한 요청
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED
                || ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED
                || ActivityCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED
                || ActivityCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED
                || ActivityCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED
                || ActivityCompat.checkSelfPermission(this, Manifest.permission.INTERNET) != PackageManager.PERMISSION_GRANTED) {

            ActivityCompat.requestPermissions(this, new String[]
                    {Manifest.permission.ACCESS_FINE_LOCATION,
                            Manifest.permission.ACCESS_COARSE_LOCATION, Manifest.permission.CAMERA,
                            Manifest.permission.WRITE_EXTERNAL_STORAGE, Manifest.permission.READ_EXTERNAL_STORAGE, Manifest.permission.INTERNET}, 1000);
        }

        // 메인의 첫화면을 리스트뷰 플레그먼트로 지정함
        listViewFragment();

        dbHelper = new DBHelper(this);
        placeList= new ArrayList<>();

        // 특정위치의 하단바가 눌릴때마다 알맞는 플래그먼트를 호출함
        bottomNavigationView = findViewById(R.id.bottom_navigation);
        bottomNavigationView.setOnNavigationItemSelectedListener(mOnNavigationListener);


        // 플로팅버튼이 눌리면, 상세페이지가 호출됨
        fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(mFabListener);

        fusedLocationProviderClient = LocationServices.getFusedLocationProviderClient(this);
        buildLocationRequest();
        buildLocationCallback();
    }

    private void buildLocationRequest() {
        locationRequest = new LocationRequest();
        locationRequest.setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY);
        locationRequest.setInterval(1000);
        locationRequest.setFastestInterval(500);
        locationRequest.setSmallestDisplacement(10f);
    }


    private void buildLocationCallback() {
        locationCallback = new LocationCallback() {
            @Override
            public void onLocationResult(final LocationResult locationResult) {
                currentLocation = locationResult.getLastLocation();
                settingDetect();
            }
        };
    }

    public View.OnClickListener mFabListener
            = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            startActivity(new Intent(MainActivity.this, AddContent.class));
        }
    };

    public BottomNavigationView.OnNavigationItemSelectedListener mOnNavigationListener
            = new BottomNavigationView.OnNavigationItemSelectedListener() {
        @Override
        public boolean onNavigationItemSelected(@NonNull MenuItem menuItem) {
            switch (menuItem.getItemId()) {
                case R.id.navigation_menu1: {
                    listViewFragment();
                    return true;
                }
                case R.id.navigation_menu2: {
                    MapFragment();
                    return true;
                }
                case R.id.navigation_menu3: {
                    GridFragment();
                    return true;
                }

            }
            return false;
        }
    };

    public void listViewFragment() {
        ListFragment fragment = ListFragment.newInstance();
        FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
        ft.replace(R.id.frame_layout, fragment);
        ft.commit();
    }

    public void MapFragment() {
        MapFragment fragment = MapFragment.newInstance();
        FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
        ft.replace(R.id.frame_layout, fragment);
        ft.commit();
    }

    public void GridFragment() {
        InfoFragment fragment = InfoFragment.newInstance();
        FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
        ft.replace(R.id.frame_layout, fragment);
        ft.commit();
    }

    private void settingDetect() {
        myDetectionRef = FirebaseDatabase.getInstance().getReference("Detection").child("isDetect");
        //myDetectionRef.setValue(true);

        myDetectionRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {

                isDetect = dataSnapshot.getValue(Boolean.class);
                if (isDetect) {
                    addDetectArea();
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });
    }

    private void addDetectArea() {
        if (fusedLocationProviderClient != null) {
            fusedLocationProviderClient.requestLocationUpdates(locationRequest, locationCallback, Looper.myLooper());
        }

        if (dbHelper == null) {
            dbHelper = new DBHelper(this);
        }
        final List<ListViewItem> itemList = MainActivity.dbHelper.getAllListViewItemData();
        LatLng latLng = new LatLng(Double.parseDouble(String.format("%.5f",currentLocation.getLatitude()))
                ,Double.parseDouble(String.format("%.5f",currentLocation.getLongitude())));
        //사용자의 현재 위치
        if (currentLocation != null){
            if(placeList==null||!placeList.contains(latLng)) {
                Uri uri = Uri.parse("android.resource://" + R.class.getPackage().getName() + "/" + R.drawable.black_mark);

                ListViewItem listViewItem = new ListViewItem();
                listViewItem.setPath(uri.getPath());
                listViewItem.setTitle("블랙아이스 의심영역");
                listViewItem.setContent("위도: " + latLng.latitude + ", 경도: " + latLng.longitude);
                listViewItem.setLatitude(latLng.latitude);
                listViewItem.setLongitude(latLng.longitude);
                MainActivity.dbHelper.addListViewItem(listViewItem);

                placeList.add(latLng);

                FirebaseDatabase.getInstance()
                        .getReference("Detection")
                        .child("Location")
                        .setValue(latLng);
                Toast.makeText(getApplicationContext(), "차량이 블랙아이스 의심영역 감지!", Toast.LENGTH_SHORT).show();
            }
            else if(placeList.contains(latLng))
            {
                Toast.makeText(getApplicationContext(), "이미 추가된 위치입니다 :)", Toast.LENGTH_SHORT).show();
            }
        }
        myDetectionRef.setValue(false);
    }

    @Override
    protected void onResume() {
        super.onResume();
        fusedLocationProviderClient.requestLocationUpdates(locationRequest, locationCallback, null);
    }

    @Override
    protected void onStop() {
        super.onStop();
        fusedLocationProviderClient.removeLocationUpdates(locationCallback);
    }

/*public static String getKeyHash(final Context context) throws PackageManager.NameNotFoundException {
        PackageManager pm = context.getPackageManager();
        PackageInfo packageInfo = pm.getPackageInfo(context.getPackageName(), PackageManager.GET_SIGNATURES);
        if (packageInfo == null) return null;
        for (Signature signature : packageInfo.signatures) {
            try {
                MessageDigest md = MessageDigest.getInstance("SHA");
                md.update(signature.toByteArray());
                return Base64.encodeToString(md.digest(), Base64.NO_WRAP);
            } catch (NoSuchAlgorithmException e) {
                Log.w("MainActivity", "Unable to get MessageDigest. signature=" + signature, e);
            }
        }
        return null;
    }*/

}
