# LunaFlow AI - Android Deployment Guide

This guide provides instructions on how to package LunaFlow AI into an Android APK while preserving our premium feminine UI, Sakura theme, and glassmorphism design.

## Recommended Approach: WebView Wrapper
Since LunaFlow AI uses Streamlit to render its complex UI/UX, the fastest and most robust way to deploy to the Google Play Store without losing ANY of the glassmorphism, responsive styling, or soft gradients is by using an **Android WebView Wrapper**. 

This approach loads the hosted web version of LunaFlow AI inside a native Android container. It ensures 100% parity with the web experience while offering native Android functionality (like push notifications).

### Step 1: Deploy LunaFlow AI to the Cloud
Before wrapping the app, you must host it online.
1. Create a GitHub repository for LunaFlow AI.
2. Deploy the app to a service like **Streamlit Community Cloud**, **Render**, or **Heroku**.
3. Obtain your live URL (e.g., `https://lunaflow-ai.streamlit.app`).

### Step 2: Build the Android Wrapper (using Android Studio)
1. Download and install **Android Studio**.
2. Create a new "Empty Views Activity" Project (Language: Kotlin/Java).
3. Open `AndroidManifest.xml` and add Internet permissions:
   ```xml
   <uses-permission android:name="android.permission.INTERNET" />
   ```
4. In `activity_main.xml`, add the WebView component:
   ```xml
   <WebView
       android:id="@+id/webview"
       android:layout_width="match_parent"
       android:layout_height="match_parent" />
   ```
5. In `MainActivity.kt` (or `.java`), initialize the WebView:
   ```kotlin
   val webView = findViewById<WebView>(R.id.webview)
   webView.settings.javaScriptEnabled = true
   webView.settings.domStorageEnabled = true
   webView.webViewClient = WebViewClient()
   webView.loadUrl("https://your-lunaflow-url.com")
   ```

### Step 3: Handle Notifications (Push)
Since LunaFlow AI now has a Notification Center and User Settings in the database, you can connect Firebase Cloud Messaging (FCM) to trigger local Android notifications.
- When the Streamlit backend detects a reminder (e.g., "Period in 3 Days"), it sends an API request to FCM.
- FCM wakes up the Android app and displays a native push notification.

### Step 4: Generate the APK / AAB
1. In Android Studio, go to **Build** -> **Generate Signed Bundle / APK**.
2. Select **Android App Bundle** (required for Play Store) or **APK** (for direct testing).
3. Create a new Keystore, fill in your developer details, and click Finish.

### Step 5: Publish to Google Play
1. Create a Google Play Developer account.
2. Setup your App Listing (Name: LunaFlow AI, Description, Sakura-themed screenshots).
3. Upload your generated `.aab` file.
4. Submit for review!

---

### Alternative: Flutter Wrapper (webview_flutter)
If you prefer Dart/Flutter for cross-platform expansion to iOS:
1. Run `flutter create lunaflow_app`
2. Add dependency: `flutter pub add webview_flutter`
3. Wrap your UI in a WebView pointing to your Streamlit host URL.
