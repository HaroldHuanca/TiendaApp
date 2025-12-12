# 🎨 Paletas de Colores Predefinidas

Este archivo contiene paletas de colores listas para usar. Solo reemplaza las variables en `estilos.css` línea 9-40.

## 📋 Cómo usar

1. Abre `app/static/css/estilos.css`
2. Busca la sección `:root { ... }` (líneas 9-67)
3. Reemplaza los colores PRIMARIOS y SECUNDARIOS
4. Recarga la página en el navegador (Ctrl+R o Cmd+R)

---

## 🎨 Paleta 1: Indigo Profesional (Actual)

```css
--primary-color: #4F46E5;
--primary-dark: #4338CA;
--primary-light: #818CF8;
--secondary-color: #10B981;
--secondary-dark: #059669;
--secondary-light: #34D399;
```

**Mejor para**: Apps profesionales, finanzas, educación

---

## 🎨 Paleta 2: Azul Corporativo

```css
--primary-color: #0066CC;
--primary-dark: #004A99;
--primary-light: #3399FF;
--secondary-color: #00AA44;
--secondary-dark: #007A33;
--secondary-light: #33BB55;
```

**Mejor para**: Empresas, banca, corporativos

---

## 🎨 Paleta 3: Rojo Energético

```css
--primary-color: #DC2626;
--primary-dark: #991B1B;
--primary-light: #EF4444;
--secondary-color: #F59E0B;
--secondary-dark: #D97706;
--secondary-light: #FBBF24;
```

**Mejor para**: Retail, comercio electrónico, energía

---

## 🎨 Paleta 4: Púrpura Moderno

```css
--primary-color: #8B5CF6;
--primary-dark: #6D28D9;
--primary-light: #A78BFA;
--secondary-color: #06B6D4;
--secondary-dark: #0891B2;
--secondary-light: #22D3EE;
```

**Mejor para**: Tech, startups, creatividad

---

## 🎨 Paleta 5: Verde Ecológico

```css
--primary-color: #059669;
--primary-dark: #047857;
--primary-light: #10B981;
--secondary-color: #0891B2;
--secondary-dark: #0E7490;
--secondary-light: #22D3EE;
```

**Mejor para**: Sostenibilidad, agronegocios, salud

---

## 🎨 Paleta 6: Naranja Cálido

```css
--primary-color: #EA580C;
--primary-dark: #C2410C;
--primary-light: #FB923C;
--secondary-color: #DC2626;
--secondary-dark: #991B1B;
--secondary-light: #EF4444;
```

**Mejor para**: Alimentos, hospitales, retail

---

## 🎨 Paleta 7: Gris Minimalista

```css
--primary-color: #374151;
--primary-dark: #1F2937;
--primary-light: #6B7280;
--secondary-color: #0891B2;
--secondary-dark: #0E7490;
--secondary-light: #22D3EE;
```

**Mejor para**: Herramientas B2B, administración, portales

---

## 🎨 Paleta 8: Rosa Moderno

```css
--primary-color: #DB2777;
--primary-dark: #BE185D;
--primary-light: #EC4899;
--secondary-color: #7C3AED;
--secondary-dark: #6D28D9;
--secondary-light: #A78BFA;
```

**Mejor para**: Belleza, moda, lifestyle

---

## 🎨 Paleta 9: Turquesa Refrescante

```css
--primary-color: #0D9488;
--primary-dark: #115E59;
--primary-light: #14B8A6;
--secondary-color: #0891B2;
--secondary-dark: #0E7490;
--secondary-light: #22D3EE;
```

**Mejor para**: Agua, turismo, bienestar

---

## 🎨 Paleta 10: Marrón Elegante

```css
--primary-color: #78350F;
--primary-dark: #54331D;
--primary-light: #A16207;
--secondary-color: #DC2626;
--secondary-dark: #991B1B;
--secondary-light: #EF4444;
```

**Mejor para**: Lujo, artesanía, antigüedades

---

## 🌈 Crear tu Paleta Personalizada

### Paso 1: Elige tu color primario
- Usa https://colorhexa.com/ o https://www.color-hex.com/
- Busca colores que te gusten

### Paso 2: Obtén variaciones
La mayoría de sitios de colores te muestran:
- El color base
- Una versión más oscura (-dark)
- Una versión más clara (-light)

### Paso 3: Reemplaza en el CSS
```css
--primary-color: #TU_COLOR_AQUI;
--primary-dark: #COLOR_MAS_OSCURO;
--primary-light: #COLOR_MAS_CLARO;
--secondary-color: #TU_COMPLEMENTARIO;
```

### Paso 4: Prueba
Recarga la página y verifica que se ve bien.

---

## 🎯 Tips para Elegir Colores

✅ **DO**:
- Usa colores con suficiente contraste (accesibilidad)
- Mantén colores consistentes en toda la app
- Prueba en diferentes dispositivos
- Considera el modo claro y oscuro

❌ **DON'T**:
- No uses más de 3 colores primarios
- Evita colores muy saturados juntos
- No ignores la accesibilidad (contraste)
- No cambies colores frecuentemente

---

## 🔗 Herramientas Útiles

- **Color Picker**: https://colordot.it/
- **Paletas Inspiración**: https://coolors.co/
- **Contraste**: https://webaim.org/resources/contrastchecker/
- **Gradientes**: https://www.gradienthunt.com/
- **Color Harmonies**: https://color.adobe.com/

---

## 📝 Ejemplo Completo

Si quieres cambiar a la Paleta 2 (Azul Corporativo):

1. Abre: `app/static/css/estilos.css`
2. Busca las líneas 14-20:
```css
--primary-color: #4F46E5;
--primary-dark: #4338CA;
--primary-light: #818CF8;
--secondary-color: #10B981;
--secondary-dark: #059669;
--secondary-light: #34D399;
```

3. Reemplaza con:
```css
--primary-color: #0066CC;
--primary-dark: #004A99;
--primary-light: #3399FF;
--secondary-color: #00AA44;
--secondary-dark: #007A33;
--secondary-light: #33BB55;
```

4. Guarda (Ctrl+S)
5. Recarga la página (F5 o Ctrl+R)

¡Listo! Toda tu app ahora usa los nuevos colores.

---

**Última actualización**: 11 de diciembre de 2025
