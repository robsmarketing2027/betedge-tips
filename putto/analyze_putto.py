#!/usr/bin/env python3
"""Puttó számgyakoriság- és véletlenszerűség-elemzés.

Usage: python3 analyze_putto.py [putto_draws.csv] > report.txt
"""
import itertools
import sys
from math import comb
import numpy as np
import pandas as pd
from scipy import stats

path = sys.argv[1] if len(sys.argv) > 1 else "putto_draws.csv"
df = pd.read_csv(path)
N = len(df)
A = df[[f"A{i}" for i in range(1, 9)]].to_numpy()
B = df["B"].to_numpy()

# Indicator matrix: X[t, k] = 1 if number k+1 drawn in field A at draw t
X = np.zeros((N, 20), dtype=np.int8)
np.put_along_axis(X, A - 1, 1, axis=1)
p = 8 / 20


def a_chi2(Xs):
    """Goodness of fit for field A. Per-draw indicators are hypergeometric, so
    Cov = p(1-p)*20/19*(I - J/20); hence 19/20 * sum(z^2) ~ chi2(19)."""
    n = len(Xs)
    z = (Xs.sum(0) - n * p) / np.sqrt(n * p * (1 - p))
    s = 19 / 20 * (z ** 2).sum()
    return s, stats.chi2.sf(s, 19), z


def section(t):
    print(f"\n## {t}\n")


print(f"# Puttó elemzés – {N:,} húzás ({df.datetime.iloc[0]} – {df.datetime.iloc[-1]})")

section("1. A mező – számgyakoriság (várható: 40% minden számra)")
cnt = X.sum(0)
s, pv, z = a_chi2(X)
last_seen = np.array([N - 1 - np.max(np.nonzero(X[:, k])[0]) for k in range(20)])
print("| Szám | Darab | Arány | Eltérés a várttól | z-érték | Utoljára (húzással ezelőtt) |")
print("|---:|---:|---:|---:|---:|---:|")
for k in np.argsort(-cnt):
    print(f"| {k+1} | {cnt[k]:,} | {cnt[k]/N:.4%} | {cnt[k]-N*p:+,.0f} | {z[k]:+.2f} | {last_seen[k]} |")
print(f"\nKhi-négyzet (df=19): {s:.2f}, p = {pv:.4f}")
print(f"Legnagyobb |z|: {np.abs(z).max():.2f} (20 számnál ±2.8-ig teljesen normális)")

section("2. B mező – számgyakoriság (várható: 25%)")
bc = np.bincount(B, minlength=5)[1:]
chi_b = stats.chisquare(bc)
print("| Szám | Darab | Arány | Eltérés | z-érték |")
print("|---:|---:|---:|---:|---:|")
for k in range(4):
    zb = (bc[k] - N / 4) / np.sqrt(N * 0.25 * 0.75)
    print(f"| {k+1} | {bc[k]:,} | {bc[k]/N:.4%} | {bc[k]-N/4:+,.0f} | {zb:+.2f} |")
print(f"\nKhi-négyzet (df=3): {chi_b.statistic:.2f}, p = {chi_b.pvalue:.4f}")

section("3. Időbeli stabilitás – évenkénti khi-négyzet próbák")
years = df.datetime.str[:4].to_numpy()
print("| Év | Húzások | A khi² p-érték | B khi² p-érték |")
print("|---|---:|---:|---:|")
for y in sorted(set(years)):
    m = years == y
    _, pa, _ = a_chi2(X[m])
    pb = stats.chisquare(np.bincount(B[m], minlength=5)[1:]).pvalue
    print(f"| {y} | {m.sum():,} | {pa:.3f} | {pb:.3f} |")

section("4. Függetlenség – befolyásolja-e az előző húzás a következőt?")
same_day = (df.datetime.str[:10].to_numpy()[1:] == df.datetime.str[:10].to_numpy()[:-1])
overlap = (X[1:] & X[:-1]).sum(1)[same_day]
hyp = stats.hypergeom(20, 8, 8)
print(f"Egymást követő húzások közös A-számai: átlag {overlap.mean():.4f} (elméleti {hyp.mean():.4f})")
obs = np.bincount(overlap, minlength=9)
exp = np.array([hyp.pmf(k) for k in range(9)]) * len(overlap)
mask = exp >= 5
o2, e2 = obs[mask], exp[mask] * obs[mask].sum() / exp[mask].sum()
print(f"Átfedés-eloszlás khi² p = {stats.chisquare(o2, e2).pvalue:.4f}")
prev_in = X[:-1][same_day] == 1
next_in = X[1:][same_day] == 1
print(f"P(szám kihúzva | előzőleg is kihúzva) = {next_in[prev_in].mean():.4%}  "
      f"P(… | előzőleg nem) = {next_in[~prev_in].mean():.4%}  (mindkettő elméletileg 40%)")
brep = (B[1:] == B[:-1])[same_day]
print(f"B szám ismétlődése egymás után: {brep.mean():.4%} (elméleti 25%)")

section("5. Számpárok (190 pár, várható együttes arány 8·7/(20·19) = 14.74%)")
pair = (X.T.astype(np.int64) @ X.astype(np.int64))
pp = 8 * 7 / (20 * 19)
iu = np.triu_indices(20, 1)
pz = (pair[iu] - N * pp) / np.sqrt(N * pp * (1 - pp))
order = np.argsort(pz)
print("Leggyakoribb párok: " + ", ".join(f"{iu[0][i]+1}-{iu[1][i]+1} (z={pz[i]:+.2f})" for i in order[::-1][:5]))
print("Legritkább párok: " + ", ".join(f"{iu[0][i]+1}-{iu[1][i]+1} (z={pz[i]:+.2f})" for i in order[:5]))
print(f"|z|>3.0 párok száma: {(np.abs(pz) > 3).sum()} (190 párnál véletlenül várható ~0.5)")

section("6. Teljes kombinációk (C(20,8) = 125 970 lehetséges A-mező)")
keys = pd.Series([tuple(r) for r in np.sort(A, 1)])
vc = keys.value_counts()
lam = N / comb(20, 8)
print(f"Különböző kihúzott kombinációk: {len(vc):,} / {comb(20, 8):,}; átlagosan {lam:.2f} előfordulás/kombináció")
print(f"Soha ki nem húzott kombinációk: {comb(20, 8) - len(vc):,} (Poisson szerint várható: {comb(20, 8) * np.exp(-lam):,.0f})")
print(f"Legtöbbször kihúzott kombináció: {[int(x) for x in vc.index[0]]} – {vc.iloc[0]}× "
      f"(Poisson szerint a maximum várhatóan ~{stats.poisson(lam).ppf(1 - 1 / comb(20, 8)):.0f})")

section("7. Visszatesztelés – 'forró' vs 'hideg' vs véletlen számok")
W = 1000
cs = np.vstack([np.zeros(20, np.int64), np.cumsum(X, 0)])
rng = np.random.default_rng(0)
idx = np.arange(W, N)
win = cs[idx] - cs[idx - W]                      # occurrences in the last W draws
tie = rng.random((len(idx), 20)) * 1e-3
hot = np.argsort(-(win + tie), 1)[:, :8]
cold = np.argsort(win + tie, 1)[:, :8]
rand = np.argsort(rng.random((len(idx), 20)), 1)[:, :8]
Xi = X[idx]
print(f"Minden húzásnál (n={len(idx):,}) 8 számot választunk az előző {W} húzás alapján, és megszámoljuk a találatokat.\n")
print("| Stratégia | Átlagos találat | 8 találat aránya |")
print("|---|---:|---:|")
for name, pick in [("Forró számok (leggyakoribb 8)", hot), ("Hideg számok (legritkább 8)", cold), ("Véletlen 8 szám", rand)]:
    h = np.take_along_axis(Xi, pick, 1).sum(1)
    print(f"| {name} | {h.mean():.4f} | {(h == 8).mean():.6%} |")
print(f"| *Elméleti érték bármely 8 számra* | {hyp.mean():.4f} | {1/comb(20,8):.6%} |")

section("8. Out-of-sample ellenőrzés (tanító: 2015–2020, teszt: 2021–)")
tr, te = years <= "2020", years >= "2021"
ftr = X[tr].mean(0)
for name, sel in [("Tanító időszak 8 leggyakoribb száma", np.argsort(-ftr)[:8]),
                  ("Tanító időszak 8 legritkább száma", np.argsort(ftr)[:8])]:
    h = X[te][:, sel].sum(1)
    zt = (h.mean() - hyp.mean()) / (hyp.std() / np.sqrt(len(h)))
    print(f"- {name} {sorted(int(k) + 1 for k in sel)}: átlagos találat a tesztidőszakban {h.mean():.4f} (z = {zt:+.1f})")

section("9. Torzítás modellje és várható visszatérülés (RTP)")
# Max-entropy model P(S) ∝ exp(sum theta_k), fitted to the observed marginals of field A.
Cmb = np.array(list(itertools.combinations(range(20), 8)))
M = np.zeros((len(Cmb), 20)); np.put_along_axis(M, Cmb, 1, axis=1)
f, th = X.mean(0), np.zeros(20)
for _ in range(200):
    lw = M @ th; P = np.exp(lw - lw.max()); P /= P.sum()
    th += np.log(f / (P @ M))
best = np.argmax(P)
MULT = {8: (10000, 1000), 7: (150, 50), 6: (24, 8), 5: (4, 2), 4: (2, 0)}  # (B talált, B nem talált)
hits = (M * M[best]).sum(1).astype(int)
p_best = {k: P[hits == k].sum() for k in MULT}
p_uni = {k: hyp.pmf(k) for k in MULT}
rtp = lambda q: sum(q[k] * (0.25 * a + 0.75 * b) for k, (a, b) in MULT.items())
u = 1 / comb(20, 8)
print(f"Modell szerinti legvalószínűbb A-kombináció: {[int(k) + 1 for k in Cmb[best]]}")
print(f"P(8 találat) = 1 : {1 / P[best]:,.0f}  (egyenletes: 1 : {comb(20, 8):,}; arány {P[best] / u:.3f}×)")
print(f"Legkevésbé valószínű: {[int(k) + 1 for k in Cmb[np.argmin(P)]]} ({P.min() / u:.3f}×)")
print(f"\nVárható visszatérülés (RTP), hivatalos nyereményszorzókkal, B mező 1/4 eséllyel:")
print(f"- Elméleti (egyenletes sorsolás): {rtp(p_uni):.2%}")
print(f"- Modell szerinti legjobb A-kombináció: {rtp(p_best):.2%}")
print(f"  → 100 Ft tétből várhatóan {100 * (1 - rtp(p_best)):.0f} Ft veszteség marad")
