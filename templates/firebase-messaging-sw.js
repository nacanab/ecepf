// Donnez le nom de votre app Firebase ici
importScripts('https://www.gstatic.com/firebasejs/9.0.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.0.0/firebase-messaging-compat.js');

firebase.initializeApp({
    apiKey: "AIzaSyBz3-DmhiHtNRrPy2bjtMWeVPs1qASY3jc",

    authDomain: "ecep-f1dc4.firebaseapp.com",
  
    projectId: "ecep-f1dc4",
  
    storageBucket: "ecep-f1dc4.firebasestorage.app",
  
    messagingSenderId: "3285729809",
  
    appId: "1:3285729809:web:8ccc6c233060d8392767b0",
  
    measurementId: "G-PJCYNKLVV2",
});

const messaging = firebase.messaging();

// Gestion des notifications en arrière-plan
messaging.onBackgroundMessage(function(payload) {
  console.log('[firebase-messaging-sw.js] Reçu message en arrière-plan ', payload);
  
  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
    icon: '/static/logo.png'  // Chemin vers votre icône
  };

  return self.registration.showNotification(notificationTitle, notificationOptions);
});