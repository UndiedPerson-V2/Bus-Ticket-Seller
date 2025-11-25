// App.js (Frontend - ฉบับตัด Register ออกแล้ว)
import React, { useState } from 'react';
import { StyleSheet, View, Text, TextInput, Button, Alert, SafeAreaView, ActivityIndicator } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

// -----------------------------------------------------------------
// ** ❗️❗️ IP Address ของ Backend Server (ห้ามลืม!) ❗️❗️ **
// -----------------------------------------------------------------
const API_URL = 'http://192.168.1.168:4000'; // << ❗️❗️ ใส่ IP ของคุณตรงนี้ ❗️❗️

// =========== หน้า Login (ฉบับคลีน) ===========
function LoginScreen({ onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // (ตามรูป) ฟังก์ชันเมื่อกดปุ่ม "Login"
  const handleLogin = async () => {
    if (!username || !password) {
      Alert.alert('ข้อผิดพลาด', 'กรุณากรอก Username และ Password');
      return;
    }

    setIsLoading(true);

    try {
      // 1. (ตามรูป) กดแล้วส่งข้อมูล... ไปยัง Backend
      const response = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      });

      const data = await response.json();

      // 2. (ตามรูป) เช็คว่าถูกหรือไม่
      if (!response.ok) {
        // ถ้า Backend ตอบว่าไม่ถูก (เช่น 401)
        Alert.alert('Login ไม่สำเร็จ', data.message || 'มีบางอย่างผิดพลาด');
      } else {
        // 3. (ตามรูป) ถ้าถูก -> ไปหน้าถัดไป
        // เก็บ Token ไว้ในเครื่อง
        await AsyncStorage.setItem('userToken', data.token);
        
        // ส่ง "ชื่อคนขับ" (data.user.fullName) ไปให้ App หลัก
        onLoginSuccess(data.user.fullName);
      }
    } catch (error) {
      console.error(error);
      Alert.alert('การเชื่อมต่อล้มเหลว', 'ไม่สามารถเชื่อมต่อเซิร์ฟเวอร์ได้');
    } finally {
      setIsLoading(false); // หยุดหมุน
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Login</Text>
      
      {/* (ตามรูป) ช่อง Username */}
      <TextInput
        style={styles.input}
        placeholder="Username"
        value={username}
        onChangeText={setUsername}
        autoCapitalize="none"
      />
      
      {/* (ตามรูป) ช่อง Password */}
      <TextInput
        style={styles.input}
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry // ทำให้เป็นจุด
      />
      
      {/* (ตามรูป) ปุ่ม Login */}
      {isLoading ? (
        <ActivityIndicator size="large" color="#0000ff" />
      ) : (
        <Button title="Login" onPress={handleLogin} />
      )}
    </View>
  );
}

// =========== หน้า Home (หน้าถัดไป) ===========
// (ส่วนนี้เหมือนเดิม ไม่ต้องแก้)
function HomeScreen({ fullName, onLogout }) {
  return (
    <View style={styles.container}>
      {/* (ตามรูป) มีฟังก์ชั่นดึงชื่อ คนขับ มาไว้แสดงหน้าถัดไป */}
      <Text style={styles.title}>ยินดีต้อนรับ</Text>
      <Text style={styles.welcomeText}>{fullName}</Text>
      <Button title="Logout" onPress={onLogout} />
    </View>
  );
}

// =========== App หลักที่คอยสลับหน้า ===========
// (ส่วนนี้เหมือนเดิม ไม่ต้องแก้)
export default function App() {
  const [userFullName, setUserFullName] = useState(null);

  // ฟังก์ชันนี้จะถูกเรียกเมื่อ Login สำเร็จ
  const handleLoginSuccess = (name) => {
    setUserFullName(name);
  };

  // ฟังก์ชัน Logout
  const handleLogout = async () => {
    await AsyncStorage.removeItem('userToken'); // ลบ Token ออกจากเครื่อง
    setUserFullName(null);
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      {/* ถ้ายังไม่มีชื่อ (ยังไม่ Login) -> โชว์หน้า Login */}
      {/* ถ้ามีชื่อแล้ว -> โชว์หน้า Home */}
      {userFullName ? (
        <HomeScreen fullName={userFullName} onLogout={handleLogout} />
      ) : (
        <LoginScreen onLoginSuccess={handleLoginSuccess} />
      )}
    </SafeAreaView>
  );
}

// =========== Style (CSS ของแอป) ===========
// (ส่วนนี้เหมือนเดิม ไม่ต้องแก้)
const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
  },
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 40,
  },
  input: {
    height: 50,
    borderColor: 'gray',
    borderWidth: 1,
    borderRadius: 8,
    marginBottom: 15,
    paddingHorizontal: 10,
    fontSize: 16,
  },
  welcomeText: {
    fontSize: 20,
    textAlign: 'center',
    marginBottom: 20, // <--- ❗️❗️ เติม Comma (,) ตรงนี้ครับ ❗️❗️
  }
});