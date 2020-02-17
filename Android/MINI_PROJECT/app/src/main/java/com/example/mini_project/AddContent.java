package com.example.mini_project;


import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.location.Address;
import android.location.Geocoder;
import android.location.Location;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.os.Looper;
import android.provider.MediaStore;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.FragmentActivity;
import android.support.v4.content.ContextCompat;
import android.support.v4.content.FileProvider;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.Toast;

import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationCallback;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationResult;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.location.LocationSettingsRequest;
import com.google.android.gms.maps.CameraUpdate;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class AddContent extends FragmentActivity implements OnMapReadyCallback {

    private GoogleMap mMap;
    private Geocoder geocoder;
    FusedLocationProviderClient mFusedLocationProviderClient;
    private LocationRequest locationRequest;
    private boolean mLocationPermissionGranted;
    private static final int PERMISSIONS_REQUEST_ACCESS_FINE_LOCATION = 1;
    private static final int UPDATE_INTERVAL_MS = 1000 * 10 * 1;  // 1분 단위 시간 갱신
    private static final int FASTEST_UPDATE_INTERVAL_MS = 1000 * 30 ; // 30초 단위로 화면 갱신

    EditText title;
    EditText content;
    EditText place;

    Button addbtn;
    Button search;
    ImageButton imagebtn;

    double latitude;
    double longitude;
    String input_title;
    String input_content;
    String realPath;

    private Marker currentMarker=null;
    private Location mCurrentLocation;

    LatLng currentLatLng;

    private static final int PICK_FROM_CAMERA = 0;
    private static final int PICK_FROM_ALBUM = 1;

    protected static final String TAG = "AddContent";

    private boolean is_search=false;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_content);

        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);


        locationRequest = new LocationRequest()
                .setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY) // 정확도를 최우선적으로 고려
                .setInterval(UPDATE_INTERVAL_MS) // 위치가 Update 되는 주기
                .setFastestInterval(FASTEST_UPDATE_INTERVAL_MS); // 위치 획득후 업데이트되는 주기

        LocationSettingsRequest.Builder builder =
                new LocationSettingsRequest.Builder();

        builder.addLocationRequest(locationRequest);
        mFusedLocationProviderClient
                = LocationServices.getFusedLocationProviderClient(this);

        title = (EditText) findViewById(R.id.message);
        content = (EditText) findViewById(R.id.message2);
        place =(EditText) findViewById(R.id.message3);

        addbtn = (Button) findViewById(R.id.add_button);
        search=(Button) findViewById(R.id.search);
        imagebtn = (ImageButton) findViewById(R.id.imageButton);

        addbtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                input_title = title.getText().toString();
                input_content = content.getText().toString();

                LatLng latLng = new LatLng(Double.parseDouble(String.format("%.5f",latitude))
                        ,Double.parseDouble(String.format("%.5f",longitude)));
                if(MainActivity.placeList==null||!MainActivity.placeList.contains(latLng))  {
                    ListViewItem listViewItem = new ListViewItem();
                    Log.e("실제경로2: ", realPath);
                    listViewItem.setPath(realPath);
                    listViewItem.setTitle(input_title);
                    listViewItem.setContent(input_content);
                    listViewItem.setLatitude(latitude);
                    listViewItem.setLongitude(longitude);

                    MainActivity.dbHelper.addListViewItem(listViewItem);
                    MainActivity.placeList.add(latLng);

                    ListFragment.itemlist = MainActivity.dbHelper.getAllListViewItemData();
                    ListFragment.adapter = new ListViewAdapter(ListFragment.itemlist, AddContent.this);
                    ListFragment.listView.setAdapter(ListFragment.adapter);
                }
                else
                {
                    Toast.makeText(getApplicationContext(),"이미 존재하는 위치입니다",Toast.LENGTH_SHORT).show();
                }
                finish();
            }
        });

        // 검색 이벤트
        search.setOnClickListener(new Button.OnClickListener(){
            @Override
            public void onClick(View v){
                is_search=true;
                String str=place.getText().toString();
                List<Address> addressList = null;
                try {
                    // editText에 입력한 텍스트(주소, 지역, 장소 등)을 지오 코딩을 이용해 변환
                    addressList = geocoder.getFromLocationName(
                            str, // 주소
                            10); // 최대 검색 결과 개수
                }
                catch (IOException e) {
                    e.printStackTrace();
                }

                System.out.println(addressList.get(0).toString());
                // 콤마를 기준으로 split
                String []splitStr = addressList.get(0).toString().split(",");
                String address = splitStr[0].substring(splitStr[0].indexOf("\"") + 1,splitStr[0].length() - 2); // 주소
                System.out.println(address);

                String latitude_S = splitStr[10].substring(splitStr[10].indexOf("=") + 1); // 위도
                String longitude_S = splitStr[12].substring(splitStr[12].indexOf("=") + 1); // 경도

                // 좌표(위도, 경도) 생성
                latitude = Double.parseDouble(latitude_S);
                longitude = Double.parseDouble(longitude_S);
                LatLng point = new LatLng(latitude, longitude);
                // 마커 생성
                MarkerOptions mOptions2 = new MarkerOptions();
                mOptions2.title("search result");
                mOptions2.snippet(address);
                mOptions2.position(point);
                // 마커 추가
                mMap.addMarker(mOptions2);
                // 해당 좌표로 화면 줌
                mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(point,15));
            }
        });

        // 이미지 버튼을 누르면, 카메라와 앨범중에서 이미지를 선택하도록 한다
        imagebtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                DialogInterface.OnClickListener cameraListener = new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        doTakePhoto();
                    }
                };
                DialogInterface.OnClickListener albumListener = new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        doTakeAlbum();
                    }
                };

                new AlertDialog.Builder(AddContent.this)
                        .setTitle("업로드할 이미지 선택")
                        .setPositiveButton("사진촬영", cameraListener)
                        .setNeutralButton("앨범선택", albumListener)
                        .show();
            }
        });

    }


    private File tempFile;

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        // 정상적으로 응답받지 못한 경우
        if (resultCode != Activity.RESULT_OK) {
            Toast.makeText(this, "취소 되었습니다.", Toast.LENGTH_SHORT).show();

            if (tempFile != null) {
                if (tempFile.exists()) {
                    if (tempFile.delete()) {
                        Log.e("경로삭제: ", tempFile.getAbsolutePath() + " 삭제 성공");
                        tempFile = null;
                    }
                }
            }
            return;
        }

        // 정상적으로 응답받았을 경우
        switch (requestCode) {
            // 앨범에서 이미지를 받아오는 경우
            case PICK_FROM_ALBUM: {
                Uri photoUri = data.getData();
                Cursor cursor = null;

                try {
                    String[] proj = {MediaStore.Images.Media.DATA};

                    assert photoUri != null;
                    cursor = getContentResolver().query(photoUri, proj, null, null, null);

                    assert cursor != null;
                    int column_index = cursor.getColumnIndexOrThrow(MediaStore.Images.Media.DATA);

                    cursor.moveToFirst();
                    tempFile = new File(cursor.getString(column_index));

                } finally {
                    if (cursor != null) {
                        cursor.close();
                    }
                }

                setImage();
                break;
            }

            // 카메라에서 이미지를 받아오는 경우
            case PICK_FROM_CAMERA: {
                setImage();
            }
        }
    }

    // 파일의 실제 경로를 저장하고, 이미지 버튼에 셋팅하는 함수
    private void setImage() {
        BitmapFactory.Options options = new BitmapFactory.Options();
        Bitmap originalBm = BitmapFactory.decodeFile(tempFile.getAbsolutePath(), options);
        realPath = tempFile.getAbsolutePath();
        imagebtn.setImageBitmap(originalBm);
    }


    @Override
    public void onMapReady(GoogleMap googleMap) {

        mMap = googleMap;
        geocoder=new Geocoder(this);

        LatLng Seoul = new LatLng(37.556503, 127.045478);
        mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(Seoul,17));

        getLocationPermission();
        updateLocationUI();
        getDeviceLocation();

        // 지도 클릭 이벤트 처리
        mMap.setOnMapClickListener(new GoogleMap.OnMapClickListener() {
            @Override
            public void onMapClick(LatLng latLng) {
                latitude = latLng.latitude;
                longitude = latLng.longitude;
                Log.e("Position", "latitude: " + latitude + "longitude: " + longitude);

                BitmapDrawable bitmapdraw=(BitmapDrawable)getResources().getDrawable(R.drawable.skull);
                Bitmap b=bitmapdraw.getBitmap();
                Bitmap skull = Bitmap.createScaledBitmap(b, 130, 130, false);
                mMap.addMarker(new MarkerOptions().position(latLng)
                        .icon(BitmapDescriptorFactory.fromBitmap(skull)));
                mMap.moveCamera(CameraUpdateFactory.newLatLng(latLng));
            }
        });

        mMap.setOnMarkerClickListener(new GoogleMap.OnMarkerClickListener() {
            @Override
            public boolean onMarkerClick(Marker marker) {
                latitude=marker.getPosition().latitude;
                longitude=marker.getPosition().longitude;
                LatLng latLng=new LatLng(latitude,longitude);

                BitmapDrawable bitmapdraw=(BitmapDrawable)getResources().getDrawable(R.drawable.skull);
                Bitmap b=bitmapdraw.getBitmap();
                Bitmap skull = Bitmap.createScaledBitmap(b, 130, 130, false);
                mMap.addMarker(new MarkerOptions().position(latLng)
                        .icon(BitmapDescriptorFactory.fromBitmap(skull)));
                mMap.moveCamera(CameraUpdateFactory.newLatLng(latLng));
                return false;
            }
        });

    }

    private void getLocationPermission() {
        if (ContextCompat.checkSelfPermission(this,
                android.Manifest.permission.ACCESS_FINE_LOCATION)
                == PackageManager.PERMISSION_GRANTED) {
            mLocationPermissionGranted = true;
        } else {
            ActivityCompat.requestPermissions(this,
                    new String[]{android.Manifest.permission.ACCESS_FINE_LOCATION},
                    PERMISSIONS_REQUEST_ACCESS_FINE_LOCATION);
        }
    }
    private void updateLocationUI() {
        if (mMap == null) {
            return;
        }
        try {
            if (mLocationPermissionGranted) {
                mMap.setMyLocationEnabled(true);
                mMap.getUiSettings().setMyLocationButtonEnabled(true);
            } else {
                mMap.setMyLocationEnabled(false);
                mMap.getUiSettings().setMyLocationButtonEnabled(false);
                mCurrentLocation = null;
            }
        } catch (SecurityException e)  {
            Log.e("Exception: %s", e.getMessage());
        }
    }

    private void getDeviceLocation() {
        try {
            if (mLocationPermissionGranted) {
                mFusedLocationProviderClient.requestLocationUpdates(locationRequest, locationCallback, Looper.myLooper());
            }
        } catch (SecurityException e)  {
            Log.e("Exception: %s", e.getMessage());
        }
    }

    LocationCallback locationCallback = new LocationCallback() {
        @Override
        public void onLocationResult(LocationResult locationResult) {
            super.onLocationResult(locationResult);

            List<Location> locationList = locationResult.getLocations();

            if (locationList.size() > 0) {
                Location location = locationList.get(locationList.size() - 1);

                LatLng currentPosition
                        = new LatLng(location.getLatitude(), location.getLongitude());

                String markerTitle = getCurrentAddress(currentPosition);
                String markerSnippet = "위도:" + String.valueOf(location.getLatitude())
                        + " 경도:" + String.valueOf(location.getLongitude());

                Log.d(TAG, "Time :" + CurrentTime() + " onLocationResult : " + markerSnippet);

                //현재 위치에 마커 생성하고 이동
                if (!is_search) setCurrentLocation(location, markerTitle, markerSnippet);
                mCurrentLocation = location;
            }
        }

    };

    private String CurrentTime(){
        Date today = new Date();
        SimpleDateFormat date = new SimpleDateFormat("yyyy/MM/dd");
        SimpleDateFormat time = new SimpleDateFormat("hh:mm:ss a");
        return time.format(today);
    }

    String getCurrentAddress(LatLng latlng) {
        // 위치 정보와 지역으로부터 주소 문자열을 구한다.
        List<Address> addressList = null ;
        Geocoder geocoder = new Geocoder( this, Locale.getDefault());

        // 지오코더를 이용하여 주소 리스트를 구한다.
        try {
            addressList = geocoder.getFromLocation(latlng.latitude,latlng.longitude,1);
        } catch (IOException e) {
            Toast. makeText( this, "위치로부터 주소를 인식할 수 없습니다. 네트워크가 연결되어 있는지 확인해 주세요.", Toast.LENGTH_SHORT ).show();
            e.printStackTrace();
            return "주소 인식 불가" ;
        }

        if (addressList.size() < 1) { // 주소 리스트가 비어있는지 비어 있으면
            return "해당 위치에 주소 없음" ;
        }

        // 주소를 담는 문자열을 생성하고 리턴
        Address address = addressList.get(0);
        StringBuilder addressStringBuilder = new StringBuilder();
        for (int i = 0; i <= address.getMaxAddressLineIndex(); i++) {
            addressStringBuilder.append(address.getAddressLine(i));
            if (i < address.getMaxAddressLineIndex())
                addressStringBuilder.append("\n");
        }

        return addressStringBuilder.toString();
    }

    public void setCurrentLocation(Location location, String markerTitle, String markerSnippet) {
        if (currentMarker != null) currentMarker.remove();
        //if (currentCircle != null) currentCircle.visible(false);

        currentLatLng = new LatLng(location.getLatitude(), location.getLongitude());
        //Toast.makeText(getActivity(),"현재 실제 위치: "+currentLatLng.latitude+", "+currentLatLng.longitude,Toast.LENGTH_SHORT).show();
        Log.e("현재 실제 위치 : ", currentLatLng.latitude+","+currentLatLng.longitude);

        MarkerOptions markerOptions = new MarkerOptions();
        markerOptions.position(currentLatLng);

        BitmapDrawable bitmapdraw=(BitmapDrawable)getResources().getDrawable(R.drawable.car);
        Bitmap b=bitmapdraw.getBitmap();
        Bitmap car = Bitmap.createScaledBitmap(b, 100, 100, false);
        markerOptions.icon(BitmapDescriptorFactory.fromBitmap(car));
        markerOptions.title(markerTitle);
        markerOptions.snippet(markerSnippet);
        markerOptions.alpha(0.5f);
        currentMarker = mMap.addMarker(markerOptions);

        /*
        CircleOptions circleOptions=new CircleOptions().center(currentLatLng)
                .radius(100)
                .fillColor(0x1AFF0000)
                .strokeColor(Color.TRANSPARENT)
                .visible(true);
        currentCircle=circleOptions;

        mMap.addCircle(circleOptions);
         */

        CameraUpdate cameraUpdate = CameraUpdateFactory.newLatLng(currentLatLng);
        mMap.moveCamera(cameraUpdate);
    }

    // 카메라로 이미지를 얻는 경우
    public void doTakePhoto() {
        Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);

        try {
            tempFile = createImageFile();
        } catch (IOException e) {
            Toast.makeText(this, "이미지 처리 오류! 다시 시도해주세요.", Toast.LENGTH_SHORT).show();
            finish();
            e.printStackTrace();
        }
        // 파일로 부터 URI를 얻어옴
        if (tempFile != null) {
            Uri photoUri = FileProvider.getUriForFile(AddContent.this, "com.miniproject.android.test.fileprovider", tempFile);
            intent.putExtra(MediaStore.EXTRA_OUTPUT, photoUri);
            startActivityForResult(intent, PICK_FROM_CAMERA);
        }
    }

    // 앨범으로 부터 이미지를 얻는 경우
    public void doTakeAlbum() {
        Intent intent = new Intent(Intent.ACTION_PICK);
        intent.setType(MediaStore.Images.Media.CONTENT_TYPE);
        startActivityForResult(intent, PICK_FROM_ALBUM);
    }

    // 이미지 파일을 생성하는 함수
    private File createImageFile() throws IOException {

        // 이미지 파일 이름
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        String imageFileName = "Soyeon_" + timeStamp + "_";

        // 이미지가 저장될 폴더 이름
        File storageDir = new File(Environment.getExternalStorageDirectory() + "/Miniproject/");
        if (!storageDir.exists()) storageDir.mkdirs();

        // 빈 파일 생성
        File image = File.createTempFile(imageFileName, ".jpg", storageDir);

        return image;
    }

    @Override
    public void onRequestPermissionsResult(int requestCode,
                                           @NonNull String permissions[],
                                           @NonNull int[] grantResults) {
        mLocationPermissionGranted = false;
        switch (requestCode) {
            case PERMISSIONS_REQUEST_ACCESS_FINE_LOCATION: {
                if (grantResults.length > 0
                        && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    mLocationPermissionGranted = true;
                }
            }
        }
        updateLocationUI();
    }


}
