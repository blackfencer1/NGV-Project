package com.example.mini_project;

import android.Manifest;
import android.os.Bundle;
import android.os.Looper;
import android.os.StrictMode;
import android.provider.CalendarContract;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.squareup.picasso.Picasso;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

import github.vatsal.easyweather.Helper.ForecastCallback;
import github.vatsal.easyweather.Helper.TempUnitConverter;
import github.vatsal.easyweather.Helper.WeatherCallback;
import github.vatsal.easyweather.WeatherMap;
import github.vatsal.easyweather.retrofit.models.ForecastResponseModel;
import github.vatsal.easyweather.retrofit.models.Weather;
import github.vatsal.easyweather.retrofit.models.WeatherResponseModel;


public class InfoFragment extends Fragment {

    public final String weather_id = "f896286d83bd49508f796a30f4e793a1"; //API 키
    TextView weather2;
    TextView weather4;
    TextView condition2;
    TextView location2;
    ImageView weatherIcon;
    private final String city = "Seoul";

    private List<Weather> weathers;

    public static InfoFragment newInstance() {

        return new InfoFragment();
    }


    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_info, null);
        StrictMode.enableDefaults();
        weather2 = (TextView) view.findViewById(R.id.weather2);
        weather4 = (TextView) view.findViewById(R.id.weather4);
        location2= (TextView) view.findViewById(R.id.location2);
        condition2= (TextView) view.findViewById(R.id.condition2);
        weatherIcon=(ImageView) view.findViewById(R.id.weathericon);

        loadWeather(city);
        weathers = new ArrayList<Weather>(); //한글로 날씨를 표시하기 위한 임시 List 컬렉션 객체 생성 (import한 패키지와 이름 충돌이 발생하므로 패키지명을 모두 작성한다.)
        return view;
    }

    @Override
    public void onActivityCreated(@Nullable Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);
    }

    private void loadWeather(String city)
    {
        WeatherMap weatherMap=new WeatherMap(getContext(),weather_id);
        weatherMap.getCityWeather(city, new WeatherCallback() {
            @Override
            public void success(WeatherResponseModel response) {
                populateWeather(response);
            }

            @Override
            public void failure(String s) {

            }
        });

        weatherMap.getCityForecast(city, new ForecastCallback() {
            @Override
            public void success(ForecastResponseModel forecastResponseModel) {

            }

            @Override
            public void failure(String s) {
                Toast.makeText(getContext(),"날씨 데이터 로드 실패", Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void populateWeather(WeatherResponseModel response)
    {
        weather2.setText(TempUnitConverter.convertToCelsius(response.getMain().getTemp()).intValue() + "°C");
        weather4.setText(response.getMain().getHumidity()+ "%");

        github.vatsal.easyweather.retrofit.models.Weather[] weather = response.getWeather();
        condition2.setText(changeKor(weather[0].getDescription()));

        if(response.getName().equals("Seoul")&& Locale.getDefault().getLanguage().equals("ko")){
            location2.setText("서울");
        }else{
            location2.setText(response.getName());
        }

        String link = weather[0].getIconLink();
        Picasso.with(getContext()).load(link).into(weatherIcon);

    }

    public String changeKor(String EngWeather)
    {
        EngWeather= EngWeather.toLowerCase();

        if(EngWeather.equals("thunderstorm with light rain"))
        {
            return "가벼운 비를 동반한 천둥구름 ";
        }
        else if(EngWeather.equals("thunderstorm with rain"))
        {
            return "비를 동반한 천둥구름";
        }
        else if(EngWeather.equals("thunderstorm with heavy rain"))
        {
            return "폭우를 동반한 천둥구름";
        }
        else if(EngWeather.equals("light thunderstorm"))
        {
            return "약한 천둥구름 ";
        }
        else if(EngWeather.equals("thunderstorm"))
        {
            return "천둥구름";
        }
        else if(EngWeather.equals("heavy thunderstorm"))
        {
            return "강한 천둥구름";
        }
        else if(EngWeather.equals("ragged thunderstorm"))
        {
            return "불규칙적 천둥구름 ";
        }
        else if(EngWeather.equals("thunderstorm with light drizzle"))
        {
            return "약한 연무를 동반한 천둥구름";
        }
        else if(EngWeather.equals("thunderstorm with drizzle"))
        {
            return "연무를 동반한 천둥구름 ";
        }
        else if(EngWeather.equals("thunderstorm with heavy drizzle"))
        {
            return "강한 안개비를 동반한 천둥구름";
        }
        else if(EngWeather.equals("light intensity drizzle"))
        {
            return "가벼운 안개비";
        }
        else if(EngWeather.equals("drizzle"))
        {
            return "안개비";
        }
        else if(EngWeather.equals("heavy intensity drizzle"))
        {
            return "강한 안개비";
        }
        else if(EngWeather.equals("light intensity drizzle rain"))
        {
            return "가벼운 안개비";
        }
        else if(EngWeather.equals("drizzle rain"))
        {
            return "적은비";
        }
        else if(EngWeather.equals("heavy intensity drizzle rain"))
        {
            return "강한 적은비";
        }
        else if(EngWeather.equals("shower rain and drizzle"))
        {
            return "소나기";
        }
        else if(EngWeather.equals("light rain"))
        {
            return "약한 비";
        }
        else if(EngWeather.equals("moderate rain"))
        {
            return "중간 비";
        }
        else if(EngWeather.equals("heavy intensity rain"))
        {
            return "강한 비";
        }
        else if(EngWeather.equals("very heavy rain"))
        {
            return "매우 강한 비";
        }
        else if(EngWeather.equals("extreme rain"))
        {
            return "극심한 비";
        }
        else if(EngWeather.equals("freezing rain"))
        {
            return "우박";
        }
        else if(EngWeather.equals("light intensity shower rain"))
        {
            return "약한 소나기";
        }
        else if(EngWeather.equals("heavy intensity shower rain"))
        {
            return "강한 소나기";
        }
        else if(EngWeather.equals("ragged shower rain"))
        {
            return "불규칙적 소나기 비";
        }
        else if(EngWeather.equals("light snow"))
        {
            return "가벼운 눈";
        }
        else if(EngWeather.equals("snow"))
        {
            return "눈";
        }
        else if(EngWeather.equals("heavy snow"))
        {
            return "강한 눈";
        }
        else if(EngWeather.equals("sleet"))
        {
            return "진눈깨비";
        }
        else if(EngWeather.equals("shower sleet"))
        {
            return "소나기를 동반한 진눈깨비";
        }
        else if(EngWeather.equals("light rain and snow"))
        {
            return "약한 비와 눈";
        }
        else if(EngWeather.equals("light shower snow"))
        {
            return "약한 소나기 눈";
        }
        else if(EngWeather.equals("shower snow"))
        {
            return "소나기 눈";
        }
        else if(EngWeather.equals("heavy shower snow"))
        {
            return "강한 소나기 눈";
        }
        else if(EngWeather.equals("mist"))
        {
            return "박무";
        }
        else if(EngWeather.equals("smoke"))
        {
            return "연기";
        }
        else if(EngWeather.equals("haze"))
        {
            return "연무";
        }
        else if(EngWeather.equals("sand, dust whirls"))
        {
            return "모래 먼지";
        }
        else if(EngWeather.equals("fog"))
        {
            return "안개";
        }
        else if(EngWeather.equals("sand"))
        {
            return "모래";
        }
        else if(EngWeather.equals("dust"))
        {
            return "먼지";
        }
        else if(EngWeather.equals("volcanic ash"))
        {
            return "화산재";
        }
        else if(EngWeather.equals("squalls"))
        {
            return "돌풍";
        }
        else if(EngWeather.equals("tornado"))
        {
            return "토네이도";
        }
        else if(EngWeather.equals("clear sky"))
        {
            return "맑은 하늘";
        }
        else if(EngWeather.equals("few clouds"))
        {
            return "구름 조금";
        }
        else if(EngWeather.equals("scattered clouds"))
        {
            return "구름 조금";
        }
        else if(EngWeather.equals("broken clouds"))
        {
            return "구름이 약간";
        }
        else if(EngWeather.equals("overcast clouds"))
        {
            return "구름 많음";
        }
        else if(EngWeather.equals("tornado"))
        {
            return "태풍";
        }
        else if(EngWeather.equals("tropical storm"))
        {
            return "태풍";
        }
        else if(EngWeather.equals("hurricane"))
        {
            return "태풍";
        }
        else if(EngWeather.equals("cold"))
        {
            return "추운 날";
        }
        else if(EngWeather.equals("hot"))
        {
            return "더운 날";
        }
        else if(EngWeather.equals("windy"))
        {
            return "강풍";
        }
        else if(EngWeather.equals("hail"))
        {
            return "우박";
        }
        else if(EngWeather.equals("calm"))
        {
            return "바람 거의 없음";
        }
        else if(EngWeather.equals("light breeze"))
        {
            return "약한 바람";
        }
        else if(EngWeather.equals("gentle breeze"))
        {
            return "약한 바람";
        }
        else if(EngWeather.equals("moderate breeze"))
        {
            return "약한 바람";
        }
        else if(EngWeather.equals("fresh breeze"))
        {
            return "약한 바람";
        }
        else if(EngWeather.equals("strong breeze"))
        {
            return "강풍";
        }
        else if(EngWeather.equals("high win"))
        {
            return "강풍";
        }
        else if(EngWeather.equals("gale"))
        {
            return "강풍";
        }
        else if(EngWeather.equals("severe gale"))
        {
            return "강풍";
        }
        else if(EngWeather.equals("storm"))
        {
            return "강풍";
        }
        else if(EngWeather.equals("violent storm"))
        {
            return "강풍";
        }
        else if(EngWeather.equals("hurricane"))
        {
            return "태풍";
        }
        return "";
    }

    @Override
    public void onStart() {
        super.onStart();
    }

    @Override
    public void onStop() {
        super.onStop();
    }

    @Override
    public void onResume() {
        super.onResume();
        loadWeather("seoul");
    }
}
