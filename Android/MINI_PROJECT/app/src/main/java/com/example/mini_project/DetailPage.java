package com.example.mini_project;


import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.location.Address;
import android.location.Geocoder;
import android.net.Uri;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentActivity;
import android.support.v4.app.FragmentManager;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;
import com.kakao.kakaolink.v2.KakaoLinkResponse;
import com.kakao.kakaolink.v2.KakaoLinkService;
import com.kakao.message.template.ContentObject;
import com.kakao.message.template.LinkObject;
import com.kakao.message.template.LocationTemplate;
import com.kakao.network.ErrorResult;
import com.kakao.network.callback.ResponseCallback;
import com.kakao.util.helper.log.Logger;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;


/**
 * A simple {@link Fragment} subclass.
 */
public class DetailPage extends FragmentActivity implements OnMapReadyCallback {

    GoogleMap mMap;
    ImageView imageView;
    TextView Title_detail;
    TextView Content_detail;
    Button Share_detail;
    Button Delete_detail;

    Intent intent;
    ListViewItem item;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_detail_page);

        SupportMapFragment supportMapFragment=(SupportMapFragment) getSupportFragmentManager().
                findFragmentById(R.id.detail_map);
        supportMapFragment.getMapAsync(this);

        imageView=(ImageView) findViewById(R.id.imageView_detail);
        Title_detail=(TextView) findViewById(R.id.textView_detail);
        Content_detail=(TextView) findViewById(R.id.textView_detail2);
        Share_detail=(Button) findViewById(R.id.button_detail);
        Delete_detail=(Button) findViewById(R.id.button_detail2);


        intent= getIntent();
        item = (ListViewItem) intent.getSerializableExtra("ITEM");


        Log.e("실제경로2: ",item.getPath());

        imageView.setImageURI(Uri.parse(item.getPath()));
        Title_detail.setText(item.getTitle());
        Content_detail.setText(item.getContent());

        Delete_detail.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                MainActivity.dbHelper.deleteListViewItem(item.get_id());

                ListFragment.itemlist = MainActivity.dbHelper.getAllListViewItemData();
                ListFragment.adapter = new ListViewAdapter(ListFragment.itemlist, DetailPage.this);
                ListFragment.listView.setAdapter(ListFragment.adapter);

                finish();
            }
        });

        Share_detail.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                LocationTemplate params = LocationTemplate.newBuilder(GPS(item.getLatitude(), item.getLongitude()),
                        ContentObject.newBuilder(item.getTitle(),
                                "https://ifh.cc/g/H7VO7.png",
                                LinkObject.newBuilder()
                                        .setWebUrl("http://developers.kakao.com")
                                        .setMobileWebUrl("http://developer.kakao.com")
                                        .build())
                                .setDescrption(item.getContent())
                                .build())
                        .setAddressTitle(item.getTitle())
                        .build();
                Map<String, String> serverCallbackArgs = new HashMap<String, String>();
                serverCallbackArgs.put("user_id", "${current_user_id}");
                serverCallbackArgs.put("product_id","${shared_product_id}");

                KakaoLinkService.getInstance().sendDefault(DetailPage.this, params,
                        serverCallbackArgs, new ResponseCallback<KakaoLinkResponse>() {
                            @Override
                            public void onFailure(ErrorResult errorResult) {
                                Logger.e(errorResult.toString());
                            }

                            @Override
                            public void onSuccess(KakaoLinkResponse result) {
                                // 템플릿 밸리데이션과 쿼터 체크가 성공적으로 끝남. 톡에서 정상적으로 보내졌는지 보장은 할 수 없다.
                                // 전송 성공 유무는 서버콜백 기능을 이용하여야 한다.
                            }
                        });
            }
        });
    }


    @Override
    public void onMapReady(GoogleMap googleMap) {

        mMap = googleMap;
        LatLng position=new LatLng(item.getLatitude(),item.getLongitude());
        mMap.addMarker(new MarkerOptions().position(position));
        mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(position,17));

    }

    // 경도와 위도를 실제주소로 맵핑하는 함수
    public String GPS(double lat, double log){
        String address = null;

        Geocoder geocoder = new Geocoder(this, Locale.getDefault());
        List<Address> list = null;

        try{
            list = geocoder.getFromLocation(lat, log, 1);
        }catch(IOException e){
            e.printStackTrace();
        }

        if(list == null){
            Log.e("getAddress", "주소 데이터 얻기 실패");
            return null;
        }
        if(list.size()>0){
            Address addr = list.get(0);
            address = addr.getAdminArea() + " "//시
                    + addr.getLocality() + " "//구
                    + addr.getThoroughfare() + " "//동
                    + addr.getFeatureName();//지번
        }
        return address;
    }
}
