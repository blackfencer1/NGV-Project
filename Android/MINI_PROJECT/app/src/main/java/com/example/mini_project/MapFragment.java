package com.example.mini_project;

import android.Manifest;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.graphics.drawable.BitmapDrawable;
import android.location.Location;
import android.os.Bundle;
import android.os.Looper;
import android.speech.tts.TextToSpeech;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;

import android.support.v4.app.NotificationCompat;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import com.firebase.geofire.GeoFire;
import com.firebase.geofire.GeoLocation;
import com.firebase.geofire.GeoQuery;
import com.firebase.geofire.GeoQueryEventListener;
import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationCallback;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationResult;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapView;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.CircleOptions;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.karumi.dexter.Dexter;
import com.karumi.dexter.PermissionToken;
import com.karumi.dexter.listener.PermissionDeniedResponse;
import com.karumi.dexter.listener.PermissionGrantedResponse;
import com.karumi.dexter.listener.PermissionRequest;
import com.karumi.dexter.listener.single.PermissionListener;

import static android.speech.tts.TextToSpeech.ERROR;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Random;


/**
 * A simple {@link Fragment} subclass.
 */
public class MapFragment extends Fragment implements OnMapReadyCallback, GeoQueryEventListener {

    private GoogleMap mMap;
    private LocationRequest locationRequest;
    private LocationCallback locationCallback;
    private FusedLocationProviderClient fusedLocationProviderClient;
    public static Marker currentUser;
    private DatabaseReference myLocationRef;
    private GeoFire geoFire;
    private List<LatLng> blackiceArea;

    private TextToSpeech TTS;

    MapView mapView;

    public static MapFragment newInstance() {
        return new MapFragment();
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             final Bundle savedInstanceState) {
        final View view = inflater.inflate(R.layout.fragment_map, null);

        TTS = new TextToSpeech(getContext(), new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status != ERROR) {
                    if (status == TextToSpeech.SUCCESS) {

                        // 한국어 설정
                        int result = TTS.setLanguage(Locale.KOREAN);

                        // tts.setPitch(5); // set pitch level
                        // tts.setSpeechRate(2); // set speech speed rate

                        // 한국어가 안된다면,
                        if (result == TextToSpeech.LANG_MISSING_DATA
                                || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                            Log.e("TTS", "Language is not supported");
                        } else {
                        }
                    } else {
                        Log.e("TTS", "Initilization Failed");
                    }
                }
            }
        });

        Dexter.withActivity(getActivity())
                .withPermission(Manifest.permission.ACCESS_FINE_LOCATION)
                .withListener(new PermissionListener() {
                    @Override
                    public void onPermissionGranted(PermissionGrantedResponse response) {

                        buildLocationRequest();
                        buildLocationCallback();
                        fusedLocationProviderClient = LocationServices.getFusedLocationProviderClient(getActivity());

                        mapView = (MapView) view.findViewById(R.id.map_second);
                        mapView.onCreate(savedInstanceState);
                        mapView.onResume();
                        mapView.getMapAsync(MapFragment.this);

                        initArea();
                        settingGeoFire();
                    }

                    @Override
                    public void onPermissionDenied(PermissionDeniedResponse response) {
                        Toast.makeText(getContext(), "위치권한이 필요합니다", Toast.LENGTH_SHORT).show();
                    }

                    @Override
                    public void onPermissionRationaleShouldBeShown(PermissionRequest permission, PermissionToken token) {

                    }
                }).check();
        return view;
    }

    @Override
    public void onActivityCreated(@Nullable Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);
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
                if (mMap != null) {
                    geoFire.setLocation("ME", new GeoLocation(locationResult.getLastLocation().getLatitude(),
                            locationResult.getLastLocation().getLongitude()), new GeoFire.CompletionListener() {
                        @Override
                        public void onComplete(String key, DatabaseError error) {
                            if (currentUser != null) currentUser.remove();
                            BitmapDrawable bitmapdraw=(BitmapDrawable)getResources().getDrawable(R.drawable.car);
                            Bitmap b=bitmapdraw.getBitmap();
                            Bitmap car = Bitmap.createScaledBitmap(b, 100, 100, false);

                            currentUser = mMap.addMarker(new MarkerOptions()
                                    .position(new LatLng(locationResult.getLastLocation().getLatitude(),
                                            locationResult.getLastLocation().getLongitude()))
                                    .title("ME")
                                    .icon(BitmapDescriptorFactory.fromBitmap(car)));
                            mMap.animateCamera(CameraUpdateFactory
                                    .newLatLngZoom(currentUser.getPosition(), 17.0f));

                        }
                    });
                }
            }
        };
    }

    private void settingGeoFire() {
        myLocationRef = FirebaseDatabase.getInstance().getReference("MyLocation");
        geoFire = new GeoFire(myLocationRef);

    }


    private void initArea() {
        blackiceArea = new ArrayList<>();

        if (MainActivity.dbHelper == null) {
            MainActivity.dbHelper = new DBHelper(getActivity());
        }
        final List<ListViewItem> itemList = MainActivity.dbHelper.getAllListViewItemData();
        if (itemList.size() != 0) {
            for (int i = 0; i < itemList.size(); i++) {
                LatLng latLng = new LatLng(itemList.get(i).getLatitude(), itemList.get(i).getLongitude());
                blackiceArea.add(latLng);
            }
        }

        FirebaseDatabase.getInstance()
                .getReference("BlackIceArea")
                .child("City")
                .setValue(blackiceArea)
                .addOnCompleteListener(new OnCompleteListener<Void>() {
                    @Override
                    public void onComplete(@NonNull Task<Void> task) {
                        //Toast.makeText(getContext(),"Update location in firebase!", Toast.LENGTH_SHORT).show();
                    }
                }).addOnFailureListener(new OnFailureListener() {
            @Override
            public void onFailure(@NonNull Exception e) {
                Toast.makeText(getContext(), "파이어베이스 업데이트 실패", Toast.LENGTH_SHORT).show();
            }
        });
    }

    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;

        mMap.getUiSettings().setZoomControlsEnabled(true);
        if (fusedLocationProviderClient != null) {
            fusedLocationProviderClient.requestLocationUpdates(locationRequest, locationCallback, Looper.myLooper());
        }
        mMap.setMyLocationEnabled(true);

        for (LatLng latLng : blackiceArea) {
            mMap.addCircle(new CircleOptions().center(latLng)
                    .radius(100) //100m
                    .strokeColor(Color.BLUE)
                    .fillColor(0X220000FF)
                    .strokeWidth(5.0f)
            );
            BitmapDrawable bitmapdraw=(BitmapDrawable)getResources().getDrawable(R.drawable.skull);
            Bitmap b=bitmapdraw.getBitmap();
            Bitmap skull = Bitmap.createScaledBitmap(b, 130, 130, false);

            mMap.addMarker(new MarkerOptions().position(latLng)
                    .icon(BitmapDescriptorFactory.fromBitmap(skull)));

            GeoQuery geoQuery = geoFire.queryAtLocation(new GeoLocation(latLng.latitude, latLng.longitude), 0.1f); //100m
            geoQuery.addGeoQueryEventListener(this);

        }
    }


    @Override
    public void onStart() {
        super.onStart();
        mapView.onStart();
    }

    @Override
    public void onStop() {
        fusedLocationProviderClient.removeLocationUpdates(locationCallback);
        super.onStop();
        if (TTS != null) {
            TTS.stop();
            TTS.shutdown();
            TTS = null;
        }
    }

    @Override
    public void onResume() {
        super.onResume();
        mapView.onResume();
        fusedLocationProviderClient.requestLocationUpdates(locationRequest, locationCallback, null);
        if (mMap != null) mMap.setMyLocationEnabled(true);
    }


    @Override
    public void onKeyEntered(String key, GeoLocation location) {
        sendNotification("ARAM", String.format("%s Entered the BlackIce area!", key));
        TTS.speak("블랙아이스 의심영역에 진입했습니다", TextToSpeech.QUEUE_ADD, null);
    }

    @Override
    public void onKeyExited(String key) {
        sendNotification("ARAM", String.format("%s Exit the BlackIce area!", key));
        TTS.speak("블랙아이스 의심영역에서 벗어났습니다", TextToSpeech.QUEUE_ADD, null);
    }

    @Override
    public void onKeyMoved(String key, GeoLocation location) {
        if (currentUser != null) {
            LatLng latLng1 = new LatLng(currentUser.getPosition().latitude, currentUser.getPosition().longitude);
            LatLng latLng2 = new LatLng(location.latitude, location.longitude);

            int dis = (int) getDistance(latLng1, latLng2);

            if (dis % 100 == 0 && dis>0) {
                Toast.makeText(getContext(), "전방 " + dis + "m 지점에서 블랙아이스 감지!", Toast.LENGTH_SHORT).show();
                TTS.speak("경고! 전방" + dis + "미터 지점에서 블랙아이스를 감지했습니다", TextToSpeech.QUEUE_ADD, null);
            }
        }
    }

    private void sendNotification(String title, String content) {
        String NOTIFICATION_CHANNEL_ID = "multiple_location";
        NotificationManager notificationManager = (NotificationManager) this.getContext().getSystemService(Context.NOTIFICATION_SERVICE);
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            NotificationChannel notificationChannel = new NotificationChannel(NOTIFICATION_CHANNEL_ID
                    , "My Notificaation", NotificationManager.IMPORTANCE_DEFAULT);
            notificationChannel.setDescription("Channel description");
            notificationChannel.enableLights(true);
            notificationChannel.setLightColor(Color.RED);
            notificationChannel.setVibrationPattern(new long[]{0, 1000, 500, 1000});
            notificationChannel.enableVibration(true);
            notificationManager.createNotificationChannel(notificationChannel);
        }

        NotificationCompat.Builder builder = new NotificationCompat.Builder(getContext(), NOTIFICATION_CHANNEL_ID);
        builder.setContentTitle(title)
                .setContentText(content)
                .setAutoCancel(false)
                .setSmallIcon(R.mipmap.ic_launcher_ice_round)
                .setLargeIcon(BitmapFactory.decodeResource(getResources(), R.mipmap.ic_launcher_ice_round));
        Notification notification = builder.build();
        notificationManager.notify(new Random().nextInt(), notification);
    }

    @Override
    public void onGeoQueryReady() {

    }

    @Override
    public void onGeoQueryError(DatabaseError error) {
        Toast.makeText(getContext(), "" + error.getMessage(), Toast.LENGTH_SHORT).show();
    }

    public double getDistance(LatLng LatLng1, LatLng LatLng2) {
        double distance = 0;

        if(LatLng1==null || LatLng2==null || LatLng1==LatLng2)
        {
            distance=0;
        }
        else {
            Location locationA = new Location("A");
            locationA.setLatitude(LatLng1.latitude);
            locationA.setLongitude(LatLng1.longitude);

            Location locationB = new Location("B");
            locationB.setLatitude(LatLng2.latitude);
            locationB.setLongitude(LatLng2.longitude);

            distance = locationA.distanceTo(locationB);
        }

        return distance;
    }

}
