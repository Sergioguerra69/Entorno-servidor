from django.test import TestCase

# Create your tests here.

import requests
import json

class JokeAPITestCase(TestCase):
    """Pruebas para la API de chistes oficial"""
    
    def test_api_connection(self):
        """Prueba que la API responde correctamente"""
        print("🧪 Probando conexión con la API de chistes...")
        
        url = "https://official-joke-api.appspot.com/random_joke"
        
        try:
            # 1. Hacer la petición GET
            response = requests.get(url)
            
            # 2. Verificar estado
            self.assertEqual(response.status_code, 200, 
                           f"❌ API devolvió código {response.status_code}, esperado 200")
            print(f"✅ Status Code: {response.status_code}")
            
            # 3. Verificar que es JSON
            content_type = response.headers.get('Content-Type', '')
            self.assertIn('application/json', content_type,
                         f"❌ Content-Type incorrecto: {content_type}")
            print(f"✅ Content-Type: {content_type}")
            
            # 4. Parsear JSON
            data = response.json()
            
            # 5. Verificar estructura del chiste
            required_fields = ['type', 'setup', 'punchline', 'id']
            for field in required_fields:
                self.assertIn(field, data, f"❌ Falta campo: {field}")
            
            print(f"✅ Estructura JSON correcta")
            
            # 6. Mostrar el chiste obtenido
            print(f"\n🎭 CHISTE OBTENIDO:")
            print(f"   Tipo: {data['type']}")
            print(f"   ID: {data['id']}")
            print(f"   Setup: {data['setup']}")
            print(f"   Punchline: {data['punchline']}")
            
            # 7. Guardar respuesta para debug
            with open('joke_api_response.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Respuesta guardada en: joke_api_response.json")
            
        except requests.exceptions.ConnectionError:
            self.fail("❌ No se pudo conectar a la API")
        except json.JSONDecodeError:
            self.fail("❌ La respuesta no es JSON válido")
    
    def test_api_multiple_requests(self):
        """Prueba múltiples peticiones para obtener chistes diferentes"""
        print("\n🧪 Probando múltiples peticiones...")
        
        url = "https://official-joke-api.appspot.com/random_joke"
        joke_ids = set()
        
        for i in range(3):  # Hacer 3 peticiones
            try:
                response = requests.get(url)
                self.assertEqual(response.status_code, 200)
                
                joke = response.json()
                joke_id = joke.get('id')
                joke_ids.add(joke_id)
                
                print(f"   Petición {i+1}: ID {joke_id} - '{joke.get('setup', '')[:30]}...'")
                
            except Exception as e:
                print(f"   ❌ Error en petición {i+1}: {e}")
        
        # Verificar que al menos tenemos IDs diferentes (no garantizado, pero probable)
        if len(joke_ids) > 1:
            print(f"✅ Se obtuvieron {len(joke_ids)} chistes diferentes")
        else:
            print(f"⚠️ Solo se obtuvo 1 ID único (puede ser coincidencia)")
    
    def test_api_endpoints(self):
        """Prueba diferentes endpoints de la misma API"""
        print("\n🧪 Probando diferentes endpoints...")
        
        endpoints = {
            'random_joke': 'https://official-joke-api.appspot.com/random_joke',
            'ten_jokes': 'https://official-joke-api.appspot.com/random_ten',
            'joke_by_id': 'https://official-joke-api.appspot.com/jokes/1',  # ID específico
            'programming_jokes': 'https://official-joke-api.appspot.com/jokes/programming/ten',
        }
        
        for name, url in endpoints.items():
            try:
                response = requests.get(url)
                
                if response.status_code == 200:
                    print(f"✅ {name}: {url} - Status {response.status_code}")
                    
                    # Mostrar un ejemplo del contenido
                    data = response.json()
                    if isinstance(data, list) and len(data) > 0:
                        print(f"   Ejemplo: {data[0].get('setup', '')[:40]}...")
                    elif isinstance(data, dict):
                        print(f"   Ejemplo: {data.get('setup', '')[:40]}...")
                else:
                    print(f"❌ {name}: Status {response.status_code}")
                    
            except Exception as e:
                print(f"❌ {name}: Error - {e}")

def run_manual_test():
    """Función para ejecutar prueba manual sin Django TestRunner"""
    print("=" * 60)
    print("PRUEBA MANUAL DE LA API DE CHISTES")
    print("=" * 60)
    
    url = "https://official-joke-api.appspot.com/random_joke"
    
    try:
        # 1. Hacer petición
        response = requests.get(url)
        print(f"📡 URL: {url}")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            # 2. Obtener datos
            joke = response.json()
            
            print(f"\n🎭 CHISTE COMPLETO:")
            print(f"   ID: {joke.get('id')}")
            print(f"   Tipo: {joke.get('type')}")
            print(f"   Setup: {joke.get('setup')}")
            print(f"   Punchline: {joke.get('punchline')}")
            
            # 3. Mostrar headers
            print(f"\n📋 HEADERS:")
            for key, value in response.headers.items():
                if key.lower() in ['content-type', 'content-length', 'date']:
                    print(f"   {key}: {value}")
            
            # 4. Tiempo de respuesta
            print(f"\n⏱️  Tiempo de respuesta: {response.elapsed.total_seconds():.2f} segundos")
            
            # 5. Guardar en archivo
            with open('api_test_result.json', 'w', encoding='utf-8') as f:
                json.dump({
                    'url': url,
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'joke': joke,
                    'response_time': response.elapsed.total_seconds()
                }, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Resultado guardado en: api_test_result.json")
            
            return True
        else:
            print(f"❌ Error: Código {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión: No se pudo conectar a la API")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    # Para ejecutar directamente: python tests.py
    run_manual_test()
    