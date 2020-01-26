package com.example.mini_project;


import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.location.Address;
import android.location.Geocoder;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.annotation.Nullable;
import android.support.v4.app.FragmentActivity;
import android.support.v4.content.FileProvider;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.Toast;

import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.maps.CameraUpdate;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

public class AddContent extends FragmentActivity implements OnMapReadyCallback {

    private GoogleMap mMap;
    private Geocoder geocoder;
    FusedLocationProviderClient mFusedLocationProviderClient;

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

    private static final int PICK_FROM_CAMERA = 0;
    private static final int PICK_FROM_ALBUM = 1;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_content);

        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);
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

                ListViewItem listViewItem=new ListViewItem();
                Log.e("실제경로2: ",realPath);
                listViewItem.setPath(realPath);
                listViewItem.setTitle(input_title);
                listViewItem.setContent(input_content);
                listViewItem.setLatitude(latitude);
                listViewItem.setLongitude(longitude);

                MainActivity.dbHelper.addListViewItem(listViewItem);
                ListFragment.itemlist=MainActivity.dbHelper.getAllListViewItemData();
                ListFragment.adapter=new ListViewAdapter(ListFragment.itemlist,AddContent.this);
                ListFragment.listView.setAdapter(ListFragment.adapter);

                finish();
            }
        });

        // 검색 이벤트
        search.setOnClickListener(new Button.OnClickListener(){
            @Override
            public void onClick(View v){
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

        // 지도 클릭 이벤트 처리
        mMap.setOnMapClickListener(new GoogleMap.OnMapClickListener() {
            @Override
            public void onMapClick(LatLng latLng) {
                latitude = latLng.latitude;
                longitude = latLng.longitude;
                Log.e("Position", "latitude: " + latitude + "longitude: " + longitude);
                mMap.addMarker(new MarkerOptions().position(latLng));
                mMap.moveCamera(CameraUpdateFactory.newLatLng(latLng));
            }
        });

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
}
