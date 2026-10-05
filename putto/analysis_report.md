# Puttó elemzés – 768,292 húzás (2015-02-02 07:05 – 2026-10-05 11:10)

## 1. A mező – számgyakoriság (várható: 40% minden számra)

| Szám | Darab | Arány | Eltérés a várttól | z-érték | Utoljára (húzással ezelőtt) |
|---:|---:|---:|---:|---:|---:|
| 20 | 311,243 | 40.5110% | +3,926 | +9.14 | 2 |
| 16 | 309,546 | 40.2902% | +2,229 | +5.19 | 0 |
| 19 | 309,499 | 40.2840% | +2,182 | +5.08 | 1 |
| 17 | 309,434 | 40.2756% | +2,117 | +4.93 | 1 |
| 18 | 309,128 | 40.2357% | +1,811 | +4.22 | 0 |
| 15 | 308,957 | 40.2135% | +1,640 | +3.82 | 4 |
| 11 | 308,007 | 40.0898% | +690 | +1.61 | 1 |
| 10 | 308,001 | 40.0891% | +684 | +1.59 | 2 |
| 9 | 307,628 | 40.0405% | +311 | +0.72 | 1 |
| 5 | 307,538 | 40.0288% | +221 | +0.52 | 0 |
| 13 | 307,513 | 40.0255% | +196 | +0.46 | 6 |
| 14 | 307,451 | 40.0175% | +134 | +0.31 | 0 |
| 8 | 306,865 | 39.9412% | -452 | -1.05 | 5 |
| 7 | 306,316 | 39.8697% | -1,001 | -2.33 | 0 |
| 6 | 306,272 | 39.8640% | -1,045 | -2.43 | 2 |
| 12 | 306,206 | 39.8554% | -1,111 | -2.59 | 4 |
| 4 | 305,716 | 39.7916% | -1,601 | -3.73 | 0 |
| 3 | 304,586 | 39.6446% | -2,731 | -6.36 | 0 |
| 2 | 304,272 | 39.6037% | -3,045 | -7.09 | 1 |
| 1 | 302,158 | 39.3285% | -5,159 | -12.01 | 0 |

Khi-négyzet (df=19): 444.02, p = 0.0000
Legnagyobb |z|: 12.01 (20 számnál ±2.8-ig teljesen normális)

## 2. B mező – számgyakoriság (várható: 25%)

| Szám | Darab | Arány | Eltérés | z-érték |
|---:|---:|---:|---:|---:|
| 1 | 192,425 | 25.0458% | +352 | +0.93 |
| 2 | 192,147 | 25.0096% | +74 | +0.19 |
| 3 | 191,730 | 24.9554% | -343 | -0.90 |
| 4 | 191,990 | 24.9892% | -83 | -0.22 |

Khi-négyzet (df=3): 1.32, p = 0.7239

## 3. Időbeli stabilitás – évenkénti khi-négyzet próbák

| Év | Húzások | A khi² p-érték | B khi² p-érték |
|---|---:|---:|---:|
| 2015 | 58,080 | 0.487 | 0.057 |
| 2016 | 64,044 | 0.000 | 0.528 |
| 2017 | 63,834 | 0.000 | 0.711 |
| 2018 | 63,834 | 0.000 | 0.029 |
| 2019 | 63,834 | 0.000 | 0.643 |
| 2020 | 64,014 | 0.000 | 0.596 |
| 2021 | 63,684 | 0.000 | 0.519 |
| 2022 | 63,726 | 0.000 | 0.758 |
| 2023 | 63,828 | 0.000 | 0.932 |
| 2024 | 69,680 | 0.000 | 0.191 |
| 2025 | 73,730 | 0.000 | 0.671 |
| 2026 | 56,004 | 0.001 | 0.513 |

## 4. Függetlenség – befolyásolja-e az előző húzás a következőt?

Egymást követő húzások közös A-számai: átlag 3.1965 (elméleti 3.2000)
Átfedés-eloszlás khi² p = 0.0903
P(szám kihúzva | előzőleg is kihúzva) = 39.9562%  P(… | előzőleg nem) = 40.0292%  (mindkettő elméletileg 40%)
B szám ismétlődése egymás után: 25.0222% (elméleti 25%)

## 5. Számpárok (190 pár, várható együttes arány 8·7/(20·19) = 14.74%)

Leggyakoribb párok: 19-20 (z=+8.20), 18-20 (z=+7.79), 17-20 (z=+7.12), 16-20 (z=+7.04), 15-20 (z=+6.26)
Legritkább párok: 1-2 (z=-10.84), 1-3 (z=-10.75), 1-4 (z=-8.96), 1-7 (z=-8.08), 2-3 (z=-8.04)
|z|>3.0 párok száma: 76 (190 párnál véletlenül várható ~0.5)

## 6. Teljes kombinációk (C(20,8) = 125 970 lehetséges A-mező)

Különböző kihúzott kombinációk: 125,687 / 125,970; átlagosan 6.10 előfordulás/kombináció
Soha ki nem húzott kombinációk: 283 (Poisson szerint várható: 283)
Legtöbbször kihúzott kombináció: [2, 9, 10, 13, 15, 16, 17, 20] – 21× (Poisson szerint a maximum várhatóan ~19)

## 7. Visszatesztelés – 'forró' vs 'hideg' vs véletlen számok

Minden húzásnál (n=767,292) 8 számot választunk az előző 1000 húzás alapján, és megszámoljuk a találatokat.

| Stratégia | Átlagos találat | 8 találat aránya |
|---|---:|---:|
| Forró számok (leggyakoribb 8) | 3.2041 | 0.000782% |
| Hideg számok (legritkább 8) | 3.1961 | 0.000782% |
| Véletlen 8 szám | 3.1993 | 0.000521% |
| *Elméleti érték bármely 8 számra* | 3.2000 | 0.000794% |

## 8. Out-of-sample ellenőrzés (tanító: 2015–2020, teszt: 2021–)

- Tanító időszak 8 leggyakoribb száma [5, 13, 15, 16, 17, 18, 19, 20]: átlagos találat a tesztidőszakban 3.2183 (z = +10.4)
- Tanító időszak 8 legritkább száma [1, 2, 3, 4, 6, 7, 8, 12]: átlagos találat a tesztidőszakban 3.1787 (z = -12.1)

## 9. Torzítás modellje és várható visszatérülés (RTP)

Modell szerinti legvalószínűbb A-kombináció: [10, 11, 15, 16, 17, 18, 19, 20]
P(8 találat) = 1 : 116,467  (egyenletes: 1 : 125,970; arány 1.082×)
Legkevésbé valószínű: [1, 2, 3, 4, 6, 7, 8, 12] (0.920×)

Várható visszatérülés (RTP), hivatalos nyereményszorzókkal, B mező 1/4 eséllyel:
- Elméleti (egyenletes sorsolás): 64.10%
- Modell szerinti legjobb A-kombináció: 66.41%
  → 100 Ft tétből várhatóan 34 Ft veszteség marad
