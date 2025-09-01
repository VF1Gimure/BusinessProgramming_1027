### Decorator — Explanation

* **Intent:** Add behavior to an object dynamically by wrapping it.
* **Unity use:** Stackable effects (buffs, weapon mods) without changing the base.
* **When:** You need combinations at runtime; avoid subclass explosion.

### Decorator — Interface Version

```csharp
namespace DecoratorIface
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using UnityEngine;

    public interface IWeapon
    {
        string Name { get; }
        float GetDamage();
        string Describe();
    }

    public sealed class BaseWeapon : IWeapon
    {
        public string Name { get; }
        private readonly float _baseDamage;

        public BaseWeapon(string name, float baseDamage)
        {
            Name = name;
            _baseDamage = baseDamage;
        }

        public float GetDamage() => _baseDamage;
        public string Describe() => $"{Name} (base {GetDamage():0.##} dmg)";
    }

    public abstract class WeaponDecorator : IWeapon
    {
        protected readonly IWeapon Inner;
        protected WeaponDecorator(IWeapon inner) { Inner = inner; }

        public virtual string Name => Inner.Name;
        public virtual float GetDamage() => Inner.GetDamage();
        public virtual string Describe() => Inner.Describe();
    }

    public sealed class FireDamageDecorator : WeaponDecorator
    {
        private readonly float _extra;
        public FireDamageDecorator(IWeapon inner, float extra) : base(inner) { _extra = extra; }
        public override float GetDamage() => base.GetDamage() + _extra;
        public override string Describe() => $"{base.Describe()} + Fire({_extra:0.##})";
    }

    public sealed class CritChanceDecorator : WeaponDecorator
    {
        private readonly float _critChance;
        private readonly float _critMulti;

        public CritChanceDecorator(IWeapon inner, float critChance, float critMulti) : base(inner)
        {
            _critChance = Mathf.Clamp01(critChance);
            _critMulti = Mathf.Max(1f, critMulti);
        }

        public override float GetDamage()
        {
            float b = base.GetDamage();
            return b * (1f + _critChance * (_critMulti - 1f));
        }

        public override string Describe() => $"{base.Describe()} + Crit({_critChance:P0} x{_critMulti:0.##})";
    }

    public sealed class LoggingDecorator : WeaponDecorator
    {
        public LoggingDecorator(IWeapon inner) : base(inner) { }
        public override float GetDamage()
        {
            float dmg = base.GetDamage();
            Debug.Log($"[WeaponCalc] {Name} -> {dmg:0.##}");
            return dmg;
        }
        public override string Describe() => $"{base.Describe()} + Log";
    }

    public static class WeaponDecorators
    {
        public static readonly Dictionary<string, Func<IWeapon, IWeapon>> Factories =
            new(StringComparer.OrdinalIgnoreCase)
            {
                { "fire", w => new FireDamageDecorator(w, 5f) },
                { "crit", w => new CritChanceDecorator(w, 0.25f, 2.0f) },
                { "log",  w => new LoggingDecorator(w) }
            };

        public static IWeapon Compose(IWeapon baseWeapon, IEnumerable<string> keys)
        {
            return keys.Aggregate(baseWeapon, (w, key) =>
            {
                if (!Factories.TryGetValue(key, out var make)) throw new ArgumentException($"Unknown key: {key}");
                return make(w);
            });
        }
    }

    public sealed class WeaponDemo : MonoBehaviour
    {
        void Start()
        {
            IWeapon sword = new BaseWeapon("Short Sword", 10f);
            var chosen = new[] { "fire", "crit", "log" };
            IWeapon modded = WeaponDecorators.Compose(sword, chosen);

            Debug.Log(modded.Describe());
            Debug.Log($"Final dmg: {modded.GetDamage():0.##}");
        }
    }
}
```

### Decorator — Abstract/Concrete Version

```csharp
namespace DecoratorAbstract
{
    using System;
    using UnityEngine;

    public abstract class Weapon
    {
        public abstract string Name { get; }
        public abstract float GetDamage();
        public abstract string Describe();
    }

    public sealed class BaseWeapon : Weapon
    {
        private readonly float _baseDamage;
        private readonly string _name;

        public BaseWeapon(string name, float baseDamage)
        {
            _name = name;
            _baseDamage = baseDamage;
        }

        public override string Name => _name;
        public override float GetDamage() => _baseDamage;
        public override string Describe() => $"{Name} (base {GetDamage():0.##} dmg)";
    }

    public abstract class WeaponDecorator : Weapon
    {
        protected readonly Weapon Inner;
        protected WeaponDecorator(Weapon inner) { Inner = inner; }

        public override string Name => Inner.Name;
        public override float GetDamage() => Inner.GetDamage();
        public override string Describe() => Inner.Describe();
    }

    public sealed class FireDamageDecorator : WeaponDecorator
    {
        private readonly float _extra;
        public FireDamageDecorator(Weapon inner, float extra) : base(inner) { _extra = extra; }
        public override float GetDamage() => base.GetDamage() + _extra;
        public override string Describe() => $"{base.Describe()} + Fire({_extra:0.##})";
    }

    public sealed class CritChanceDecorator : WeaponDecorator
    {
        private readonly float _critChance;
        private readonly float _critMulti;

        public CritChanceDecorator(Weapon inner, float critChance, float critMulti) : base(inner)
        {
            _critChance = Mathf.Clamp01(critChance);
            _critMulti = Mathf.Max(1f, critMulti);
        }

        public override float GetDamage()
        {
            float b = base.GetDamage();
            return b * (1f + _critChance * (_critMulti - 1f));
        }

        public override string Describe() => $"{base.Describe()} + Crit({_critChance:P0} x{_critMulti:0.##})";
    }

    public sealed class LoggingDecorator : WeaponDecorator
    {
        public LoggingDecorator(Weapon inner) : base(inner) { }
        public override float GetDamage()
        {
            float dmg = base.GetDamage();
            Debug.Log($"[WeaponCalc] {Name} -> {dmg:0.##}");
            return dmg;
        }
        public override string Describe() => $"{base.Describe()} + Log";
    }

    public static class WeaponDecorators
    {
        public static Weapon Compose(Weapon baseWeapon, params Func<Weapon, Weapon>[] steps)
        {
            Weapon w = baseWeapon;
            foreach (var step in steps) w = step(w);
            return w;
        }
    }

    public sealed class WeaponDemo : MonoBehaviour
    {
        void Start()
        {
            Weapon sword = new BaseWeapon("Short Sword", 10f);
            Weapon modded = WeaponDecorators.Compose(
                sword,
                w => new FireDamageDecorator(w, 5f),
                w => new CritChanceDecorator(w, 0.25f, 2.0f),
                w => new LoggingDecorator(w)
            );

            Debug.Log(modded.Describe());
            Debug.Log($"Final dmg: {modded.GetDamage():0.##}");
        }
    }
}
```

### Factory Method — Explanation

* **Intent:** Let subclasses decide which product to create via a single factory method.
* **Unity use:** Spawners that produce one product type per subclass.
* **When:** You vary one product at a time.

### Factory Method — Interface Version

```csharp
namespace FactoryMethodIface
{
    using UnityEngine;

    public interface IEnemy { void Spawn(); }

    public sealed class Goblin : IEnemy { public void Spawn() => Debug.Log("Goblin spawned"); }
    public sealed class Orc    : IEnemy { public void Spawn() => Debug.Log("Orc spawned"); }

    public abstract class EnemySpawner
    {
        public abstract IEnemy CreateEnemy();
        public void SpawnEnemy()
        {
            var e = CreateEnemy();
            e.Spawn();
        }
    }

    public sealed class GoblinSpawner : EnemySpawner { public override IEnemy CreateEnemy() => new Goblin(); }
    public sealed class OrcSpawner    : EnemySpawner { public override IEnemy CreateEnemy() => new Orc(); }

    public sealed class SpawnerTest : MonoBehaviour
    {
        void Start()
        {
            EnemySpawner s = new GoblinSpawner(); s.SpawnEnemy();
            s = new OrcSpawner(); s.SpawnEnemy();
        }
    }
}
```

### Factory Method — Abstract/Concrete Version

```csharp
namespace FactoryMethodAbstract
{
    using UnityEngine;

    public abstract class Enemy { public abstract void Spawn(); }
    public sealed class Goblin : Enemy { public override void Spawn() => Debug.Log("Goblin spawned"); }
    public sealed class Orc    : Enemy { public override void Spawn() => Debug.Log("Orc spawned"); }

    public abstract class EnemySpawner
    {
        public abstract Enemy CreateEnemy();
        public void SpawnEnemy()
        {
            Enemy e = CreateEnemy();
            e.Spawn();
        }
    }

    public sealed class GoblinSpawner : EnemySpawner { public override Enemy CreateEnemy() => new Goblin(); }
    public sealed class OrcSpawner    : EnemySpawner { public override Enemy CreateEnemy() => new Orc(); }

    public sealed class SpawnerTest : MonoBehaviour
    {
        void Start()
        {
            EnemySpawner s = new GoblinSpawner(); s.SpawnEnemy();
            s = new OrcSpawner(); s.SpawnEnemy();
        }
    }
}
```

### Abstract Factory — Explanation

* **Intent:** Produce families of related products together.
* **Unity use:** Level/theme factory that returns matching sets (enemy, weapon, props).
* **When:** You vary multiple related products together.

### Abstract Factory — Interface Version

```csharp
namespace AbstractFactoryIface
{
    using UnityEngine;

    public interface IEnemy { void Spawn(); }
    public interface IWeapon { void Equip(); }

    public sealed class Goblin : IEnemy { public void Spawn() => Debug.Log("Goblin spawned"); }
    public sealed class Orc    : IEnemy { public void Spawn() => Debug.Log("Orc spawned"); }

    public sealed class GoblinClub : IWeapon { public void Equip() => Debug.Log("Club equipped"); }
    public sealed class OrcAxe     : IWeapon { public void Equip() => Debug.Log("Axe equipped"); }

    public interface ILevelFactory
    {
        IEnemy CreateEnemy();
        IWeapon CreateWeapon();
    }

    public sealed class GoblinLevelFactory : ILevelFactory
    {
        public IEnemy  CreateEnemy()  => new Goblin();
        public IWeapon CreateWeapon() => new GoblinClub();
    }

    public sealed class OrcLevelFactory : ILevelFactory
    {
        public IEnemy  CreateEnemy()  => new Orc();
        public IWeapon CreateWeapon() => new OrcAxe();
    }

    public sealed class LevelLoader : MonoBehaviour
    {
        void Start()
        {
            ILevelFactory f = new GoblinLevelFactory();
            var e = f.CreateEnemy();
            var w = f.CreateWeapon();
            e.Spawn();
            w.Equip();
        }
    }
}
```

### Abstract Factory — Abstract/Concrete Version

```csharp
namespace AbstractFactoryAbstract
{
    using UnityEngine;

    public abstract class Enemy { public abstract void Spawn(); }
    public abstract class Weapon { public abstract void Equip(); }

    public sealed class Goblin : Enemy { public override void Spawn() => Debug.Log("Goblin spawned"); }
    public sealed class Orc    : Enemy { public override void Spawn() => Debug.Log("Orc spawned"); }

    public sealed class GoblinClub : Weapon { public override void Equip() => Debug.Log("Club equipped"); }
    public sealed class OrcAxe     : Weapon { public override void Equip() => Debug.Log("Axe equipped"); }

    public abstract class LevelFactory
    {
        public abstract Enemy  CreateEnemy();
        public abstract Weapon CreateWeapon();
    }

    public sealed class GoblinLevelFactory : LevelFactory
    {
        public override Enemy  CreateEnemy()  => new Goblin();
        public override Weapon CreateWeapon() => new GoblinClub();
    }

    public sealed class OrcLevelFactory : LevelFactory
    {
        public override Enemy  CreateEnemy()  => new Orc();
        public override Weapon CreateWeapon() => new OrcAxe();
    }

    public sealed class LevelLoader : MonoBehaviour
    {
        void Start()
        {
            LevelFactory f = new GoblinLevelFactory();
            Enemy e = f.CreateEnemy();
            Weapon w = f.CreateWeapon();
            e.Spawn();
            w.Equip();
        }
    }
}
```

### Composite — Explanation

* **Intent:** Treat single objects and groups uniformly via a common type.
* **Unity use:** Units vs squads, single UI element vs panel, single effect vs group.
* **When:** You need the same operation to apply to one or many.

### Composite — Interface Version

```csharp
namespace CompositeIface
{
    using System.Collections.Generic;
    using UnityEngine;

    public interface IUnit
    {
        void Move(Vector3 destination);
    }

    public sealed class Soldier : IUnit
    {
        private readonly string _name;
        public Soldier(string name) { _name = name; }
        public void Move(Vector3 destination) => Debug.Log($"{_name} -> {destination}");
    }

    public sealed class Squad : IUnit
    {
        private readonly List<IUnit> _members = new();
        public void Add(IUnit u)    => _members.Add(u);
        public void Remove(IUnit u) => _members.Remove(u);

        public void Move(Vector3 destination)
        {
            foreach (var u in _members) u.Move(destination);
        }
    }

    public sealed class CompositeIfaceDemo : MonoBehaviour
    {
        void Start()
        {
            IUnit a = new Soldier("Alpha");
            IUnit b = new Soldier("Bravo");

            var squad = new Squad();
            squad.Add(a);
            squad.Add(b);

            a.Move(new Vector3(0,0,0));
            squad.Move(new Vector3(10,0,5));
        }
    }
}
```

### Composite — Abstract/Concrete Version

```csharp
namespace CompositeAbstract
{
    using System.Collections.Generic;
    using UnityEngine;

    public abstract class Unit
    {
        public abstract void Move(Vector3 destination);
    }

    public sealed class Soldier : Unit
    {
        private readonly string _name;
        public Soldier(string name) { _name = name; }
        public override void Move(Vector3 destination) => Debug.Log($"{_name} -> {destination}");
    }

    public sealed class Squad : Unit
    {
        private readonly List<Unit> _members = new();
        public void Add(Unit u)    => _members.Add(u);
        public void Remove(Unit u) => _members.Remove(u);

        public override void Move(Vector3 destination)
        {
            foreach (var u in _members) u.Move(destination);
        }
    }

    public sealed class CompositeAbstractDemo : MonoBehaviour
    {
        void Start()
        {
            Unit a = new Soldier("Charlie");
            Unit b = new Soldier("Delta");

            var squad = new Squad();
            squad.Add(a);
            squad.Add(b);

            b.Move(new Vector3(2,0,1));
            squad.Move(new Vector3(-5,0,7));
        }
    }
}
```
# Proxy in Unity — why it’s more useful than it looks

* **Controls access**: put checks (distance, keys, authority) before the real action runs.
* **Defers creation**: lazily load/spawn heavy stuff on first use.
* **Swappable**: caller talks to one API; you can switch the real implementation later.
* **Clean split**: proxy handles *when/how*; real subject handles *what*.
* **Fits gameplay**: doors, guards, NPCs, interactables, stage-based bosses, streamed props, network stubs.

---

## Chest Proxy (Protection + Virtual) — interface version

```csharp
// Namespace: ProxyIface
namespace ProxyIface
{
    using UnityEngine;

    // Subject interface (what callers use)
    public interface IChest
    {
        /// Returns true if opened.
        bool Open(Transform opener);
    }

    // Real subject: does actual work (animation, loot)
    public sealed class RealChest : MonoBehaviour, IChest
    {
        [SerializeField] Animator anim;
        [SerializeField] string lootId = "gold_small";

        public bool Open(Transform opener)
        {
            if (anim != null) anim.SetTrigger("Open");
            Debug.Log($"[RealChest] Open -> loot: {lootId}");
            // Spawn loot, mark opened, disable collider, etc.
            return true;
        }
    }

    // Proxy: guards access + lazily creates the real chest on first use
    public sealed class ChestProxy : MonoBehaviour, IChest
    {
        [Header("Rules")]
        [SerializeField] float openDistance = 2.0f;
        [SerializeField] string requiredKeyId = "Key_Red";

        [Header("Lazy (Virtual)")]
        [SerializeField] GameObject realChestPrefab; // must contain RealChest
        [SerializeField] Transform spawnParent;

        private RealChest real;    // cached real subject
        private bool spawned;

        public bool Open(Transform opener)
        {
            // Protection checks
            if (opener == null) return false;
            if (Vector3.Distance(opener.position, transform.position) > openDistance) return false;
            if (!Inventory.Has(requiredKeyId)) return false; // replace with real inventory

            // Virtual: spawn real chest once
            if (!spawned)
            {
                var go = Object.Instantiate(realChestPrefab, transform.position, transform.rotation, spawnParent);
                real = go.GetComponent<RealChest>();
                spawned = true;
            }

            // Delegate to real chest
            return real.Open(opener);
        }
    }

    // Minimal inventory stub for the example
    public static class Inventory
    {
        public static bool Has(string id) => true; // plug in your real check
    }

    // Example usage
    public sealed class OpenChestOnE : MonoBehaviour
    {
        [SerializeField] ChestProxy chest;
        [SerializeField] Transform player;

        void Update()
        {
            if (Input.GetKeyDown(KeyCode.E))
            {
                if (!chest.Open(player))
                    Debug.Log("Chest denied: too far or missing key.");
            }
        }
    }
}
```

---

## Chest Proxy (Protection + Virtual) — abstract/concrete classes

```csharp
// Namespace: ProxyAbstract
namespace ProxyAbstract
{
    using UnityEngine;

    // Subject base
    public abstract class Chest : MonoBehaviour
    {
        public abstract bool Open(Transform opener);
    }

    // Real subject
    public sealed class RealChest : Chest
    {
        [SerializeField] Animator anim;
        [SerializeField] string lootId = "gold_small";

        public override bool Open(Transform opener)
        {
            if (anim != null) anim.SetTrigger("Open");
            Debug.Log($"[RealChest] Open -> {lootId}");
            return true;
        }
    }

    // Proxy subject
    public sealed class ChestProxy : Chest
    {
        [Header("Rules")]
        [SerializeField] float openDistance = 2.0f;
        [SerializeField] string requiredKeyId = "Key_Red";

        [Header("Lazy (Virtual)")]
        [SerializeField] GameObject realChestPrefab; // has RealChest
        [SerializeField] Transform spawnParent;

        private RealChest real;
        private bool spawned;

        public override bool Open(Transform opener)
        {
            if (opener == null) return false;
            if (Vector3.Distance(opener.position, transform.position) > openDistance) return false;
            if (!Inventory.Has(requiredKeyId)) return false;

            if (!spawned)
            {
                var go = Object.Instantiate(realChestPrefab, transform.position, transform.rotation, spawnParent);
                real = go.GetComponent<RealChest>();
                spawned = true;
            }

            return real.Open(opener);
        }
    }

    // Minimal inventory stub
    public static class Inventory
    {
        public static bool Has(string id) => true;
    }

    // Example usage
    public sealed class ProxyAbstractDemo : MonoBehaviour
    {
        [SerializeField] Chest chest;   // drag the ChestProxy here
        [SerializeField] Transform player;

        void Update()
        {
            if (Input.GetKeyDown(KeyCode.E))
                chest.Open(player);
        }
    }
}
```

---

## Note: multi-stage boss via Proxy (for later search)

* **Idea:** One `IBoss`/`Boss` proxy holds HP, thresholds, cooldowns; **stages** are real subjects implementing the same API.
* **Proxy** decides *when to swap* active stage (HP %, timers, phase flags), optionally **lazy-creates** the next stage.
* **Keywords to search:**

  * “Unity boss phases pattern”, “stage-based boss proxy”, “delegate boss stages”, “proxy vs state pattern boss”.
* **Extensions:**

  * Stage 1/2/3 classes (different attacks/AI).
  * Cutscene or invulnerability windows inside the proxy during swaps.
  * Network: client-side proxy that forwards to server authority for stage changes.

Copy this markdown into your converter to make the PDF.

