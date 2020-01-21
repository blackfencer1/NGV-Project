package com.example.mini_project;

import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.net.Uri;
import android.util.Log;
import android.widget.Toast;

import com.google.android.gms.maps.model.LatLng;

import java.util.ArrayList;
import java.util.List;

public class DBHelper extends SQLiteOpenHelper {
    static final String DATABASE_NAME = "MINI";
    static final int DATABASE_VERSION = 1;
    Context context;

    public DBHelper(Context context) {
        super(context,DATABASE_NAME,null,DATABASE_VERSION);
        this.context=context;
    }

    // 디비가 존재하지 않을때 딱 한번만 실행된다 (DB를 만드는 역할)
    @Override
    public void onCreate(SQLiteDatabase db) {
        // String 보다 StringBuffer가 Query 만들기 편하다.
        StringBuffer sb = new StringBuffer();
        sb.append(" CREATE TABLE MINI ( ");
        sb.append(" _ID INTEGER PRIMARY KEY AUTOINCREMENT, ");
        sb.append(" PATH TEXT, ");
        sb.append(" TITLE TEXT, ");
        sb.append(" CONTENT TEXT, ");
        sb.append(" LAT DOUBLE, ");
        sb.append(" LON DOUBLE ) ");

        // SQLite Database로 쿼리 실행
        db.execSQL(sb.toString());
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        Toast.makeText(context, "The version is upgraded.", Toast.LENGTH_SHORT).show();
    }

    public void addListViewItem(ListViewItem listViewItem) {
        SQLiteDatabase db = getWritableDatabase();

        StringBuffer sb = new StringBuffer();
        sb.append(" INSERT INTO MINI ( ");
        sb.append(" PATH, TITLE, CONTENT, LAT, LON ) ");
        sb.append(" VALUES ( ?, ?, ?, ?, ? ) ");

        db.execSQL(sb.toString(),
                new Object[]{
                        listViewItem.getPath(),
                        listViewItem.getTitle(),
                        listViewItem.getContent(),
                        listViewItem.getLatitude(),
                        listViewItem.getLongitude()});
        Toast.makeText(context, "Insert 완료", Toast.LENGTH_SHORT).show();
    }

    public List<ListViewItem> getAllListViewItemData() {
        StringBuffer sb = new StringBuffer();
        sb.append(" SELECT _ID, PATH, TITLE, CONTENT, LAT, LON FROM MINI");

        SQLiteDatabase db = getReadableDatabase();

        Cursor cursor = db.rawQuery(sb.toString(), null);

        List<ListViewItem> listView = new ArrayList();
        ListViewItem listViewItem = null;

        // moveToNext 다음에 데이터가 있으면 true 없으면 false
        while( cursor.moveToNext() ) {
            listViewItem = new ListViewItem();
            listViewItem.set_id(cursor.getInt(0));
            listViewItem.setPath(cursor.getString(1));
            listViewItem.setTitle(cursor.getString(2));
            listViewItem.setContent(cursor.getString(3));
            listViewItem.setLatitude(cursor.getDouble(4));
            listViewItem.setLongitude(cursor.getDouble(5));

            listView.add(listViewItem);
        }
        return listView;
    }

    public ListViewItem getItemById(int _id) {
        StringBuffer sb = new StringBuffer();
        sb.append(" SELECT PATH, TITLE, CONTENT, LAT, LON FROM MINI WHERE _ID = ? ");

        // 읽기 전용 DB 객체를 만든다.
        SQLiteDatabase db = getReadableDatabase();
        Cursor cursor = db.rawQuery(sb.toString(), new String[]{_id + ""});

        ListViewItem listViewItem = new ListViewItem();
        if(cursor.moveToNext()) {
            listViewItem.setPath(cursor.getString(0));
            listViewItem.setTitle(cursor.getString(1));
            listViewItem.setContent(cursor.getString(2));
            listViewItem.setLatitude(cursor.getDouble(3));
            listViewItem.setLongitude(cursor.getDouble(4));
        }
        return listViewItem;
    }

    public void deleteListViewItem(int _id){
        StringBuffer sb = new StringBuffer();
        sb.append("DELETE FROM MINI WHERE _ID = "+Integer.toString(_id));
        Log.e(" 삭제할 ID 확인: ", Integer.toString(_id));
        SQLiteDatabase db = getWritableDatabase();

        db.execSQL(sb.toString());
        Toast.makeText(context, "아이템 삭제", Toast.LENGTH_SHORT).show();
    }

}
