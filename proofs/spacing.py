basic_test = r"""nnonnoonoo nnannooaoo nnbnnooboo nncnnoocoo nndnnoodoo nnennooeoo nnfnnoofoo nngnnoogoo nnhnnoohoo nninnooioo nnjnnoojoo nnknnookoo nnlnnooloo nnmnnoomoo nnpnnoopoo nnqnnooqoo nnrnnooroo nnsnnoosoo nntnnootoo nnunnoouoo nnvnnoovoo nnwnnoowoo nnxnnooxoo nnynnooyoo nnznnoozoo

HHOHHOOHOO HHAHHOOAOO HHBHHOOBOO HHCHHOOCOO HHDHHOODOO HHEHHOOEOO HHFHHOOFOO HHGHHOOGOO HHIHHOOIOO HHJHHOOJOO HHKHHOOKOO HHLHHOOLOO HHMHHOOMOO HHNHHOONOO HHPHHOOPOO HHQHHOOQOO HHRHHOOROO HHSHHOOSOO HHTHHOOTOO HHUHHOOUOO HHVHHOOVOO HHWHHOOWOO HHXHHOOXOO HHYHHOOYOO HHZHHOOZOO

010N1N 020N2N 030N3N 040N4N 050N5N 060N6N 070N7N 080N8N 090N9N

nn0nnnn1nnnn2nnnn3nnnn4nnnn5nnnn6nnnn7nnnn8nnnn9nn

oo0oooo1oooo2oooo3oooo4oooo5oooo6oooo7oooo8oooo9oo

NN0NNNN1NNNN2NNNN3NNNN4NNNN5NNNN6NNNN7NNNN8NNNN9NN

OO0OOOO1OOOO2OOOO3OOOO4OOOO5OOOO6OOOO7OOOO8OOOO9OO

000000100200300400500600700800900
"""

lc_text = "lynx tuft frogs, dolphins abduct by proxy the ever awkward klutz, dud, dummkopf, jinx snubnose filmgoer, orphan sgt. renfruw grudgek reyfus, md. sikh psych if halt tympany jewelry sri heh! twyer vs jojo pneu fylfot alcaaba son of nonplussed halfbreed bubbly playboy guggenheim daddy coccyx sgraffito effect, vacuum dirndle impossible attempt to disvalue, muzzle the afghan czech czar and exninja, bob bixby dvorak wood dhurrie savvy, dizzy eye aeon circumcision uvula scrungy picnic luxurious special type carbohydrate ovoid adzuki kumquat bomb? afterglows gold girl pygmy gnome lb. ankhs acme aggroupment akmed brouhha tv wt. ujjain ms. oz abacus mnemonics bhikku khaki bwana aorta embolism vivid owls often kvetch otherwise, wysiwyg densfort wright you’ve absorbed rhythm, put obstacle kyaks krieg kern wurst subject enmity equity coquet quorum pique tzetse hepzibah sulfhydryl briefcase ajax ehler kafka fjord elfship halfdressed jugful eggcup hummingbirds swingdevil bagpipe legwork reproachful hunchback archknave baghdad wejh rijswijk rajbansi rajput ajdir okay weekday obfuscate subpoena liebknecht marcgravia ecbolic arcticward dickcissel pincpinc boldface maidkin adjective adcraft adman dwarfness applejack darkbrown kiln palzy always farmland flimflam unbossy nonlineal stepbrother lapdog stopgap sx countdown basketball beaujolais vb. flowchart aztec lazy bozo syrup tarzan annoying dyke yucky hawg gagzhukz cuzco squire when hiho mayhem nietzsche szasz gumdrop milk emplotment ambidextrously lacquer byway ecclesiastes stubchen hobgoblins crabmill aqua hawaii blvd. subquality byzantine empire debt obvious cervantes jekabzeel anecdote flicflac mechanicville bedbug couldn’t i’ve it’s they’ll they’d dpt. headquarter burkhardt xerxes atkins govt. ebenezer lg. lhama amtrak amway fixity axmen quumbabda upjohn hrumpf"

uc_text = "LYNX TUFT FROGS, DOLPHINS ABDUCT BY PROXY THE EVER AWKWARD KLUTZ, DUD, DUMMKOPF, JINX SNUBNOSE FILMGOER, ORPHAN SGT. RENFRUW GRUDGEK REYFUS, MD. SIKH PSYCH IF HALT TYMPANY JEWELRY SRI HEH! TWYER VS JOJO PNEU FYLFOT ALCAABA SON OF NONPLUSSED HALFBREED BUBBLY PLAYBOY GUGGENHEIM DADDY COCCYX SGRAFFITO EFFECT, VACUUM DIRNDLE IMPOSSIBLE ATTEMPT TO DISVALUE, MUZZLE THE AFGHAN CZECH CZAR AND EXNINJA, BOB BIXBY DVORAK WOOD DHURRIE SAVVY, DIZZY EYE AEON CIRCUMCISION UVULA SCRUNGY PICNIC LUXURIOUS SPECIAL TYPE CARBOHYDRATE OVOID ADZUKI KUMQUAT BOMB? AFTERGLOWS GOLD GIRL PYGMY GNOME LB. ANKHS ACME AGGROUPMENT AKMED BROUHHA TV WT. UJJAIN MS. OZ ABACUS MNEMONICS BHIKKU KHAKI BWANA AORTA EMBOLISM VIVID OWLS OFTEN KVETCH OTHERWISE, WYSIWYG DENSFORT WRIGHT YOU’VE ABSORBED RHYTHM, PUT OBSTACLE KYAKS KRIEG KERN WURST SUBJECT ENMITY EQUITY COQUET QUORUM PIQUE TZETSE HEPZIBAH SULFHYDRYL BRIEFCASE AJAX EHLER KAFKA FJORD ELFSHIP HALFDRESSED JUGFUL EGGCUP HUMMINGBIRDS SWINGDEVIL BAGPIPE LEGWORK REPROACHFUL HUNCHBACK ARCHKNAVE BAGHDAD WEJH RIJSWIJK RAJBANSI RAJPUT AJDIR OKAY WEEKDAY OBFUSCATE SUBPOENA LIEBKNECHT MARCGRAVIA ECBOLIC ARCTICWARD DICKCISSEL PINCPINC BOLDFACE MAIDKIN ADJECTIVE ADCRAFT ADMAN DWARFNESS APPLEJACK DARKBROWN KILN PALZY ALWAYS FARMLAND FLIMFLAM UNBOSSY NONLINEAL STEPBROTHER LAPDOG STOPGAP SX COUNTDOWN BASKETBALL BEAUJOLAIS VB. FLOWCHART AZTEC LAZY BOZO SYRUP TARZAN ANNOYING DYKE YUCKY HAWG GAGZHUKZ CUZCO SQUIRE WHEN HIHO MAYHEM NIETZSCHE SZASZ GUMDROP MILK EMPLOTMENT AMBIDEXTROUSLY LACQUER BYWAY ECCLESIASTES STUBCHEN HOBGOBLINS CRABMILL AQUA HAWAII BLVD. SUBQUALITY BYZANTINE EMPIRE DEBT OBVIOUS CERVANTES JEKABZEEL ANECDOTE FLICFLAC MECHANICVILLE BEDBUG COULDN’T I’VE IT’S THEY’LL THEY’D DPT. HEADQUARTER BURKHARDT XERXES ATKINS GOVT. EBENEZER LG. LHAMA AMTRAK AMWAY FIXITY AXMEN QUUMBABDA UPJOHN HRUMPF"

ul_text = "Aaron Abraham Adam Aeneas Agfa Ahoy Aileen Akbar Alanon Americanism Anglican Aorta April Fool’s Day Aqua Lung (Tm.) Arabic Ash Wednesday Authorized Version Ave Maria Away Axel Ay Aztec Bhutan Bill Bjorn Bk Btu. Bvart Bzonga California Cb Cd Cervantes Chicago Clute City, Tx. Cmdr. Cnossus Coco Cracker State, Georgia Cs Ct. Cwacker Cyrano David Debra Dharma Diane Djakarta Dm Dnepr Doris Dudley Dwayne Dylan Dzerzhinsk Eames Ectomorph Eden Eerie Effingham, Il. Egypt Eiffel Tower Eject Ekland Elmore Entreaty Eolian Epstein Equine Erasmus Eskimo Ethiopia Europe Eva Ewan Exodus Jan van Eyck Ezra Fabian February Fhara Fifi Fjord Florida Fm France Fs Ft. Fury Fyn Gabriel Gc Gdynia Gehrig Ghana Gilligan Karl Gjellerup Gk. Glen Gm Gnosis Gp.E. Gregory Gs Gt. Br. Guinevere Gwathmey Gypsy Gzags Hebrew Hf Hg Hileah Horace Hrdlicka Hsia Hts. Hubert Hwang Hai Hyacinth Hz. Iaccoca Ibsen Iceland Idaho If Iggy Ihre Ijit Ike Iliad Immediate Innocent Ione Ipswitch Iquarus Ireland Island It Iud Ivert Iwerks Ixnay Iy Jasper Jenks Jherry Jill Jm Jn Jorge Jr. Julie Kerry Kharma Kiki Klear Koko Kruse Kusack Kylie Laboe Lb. Leslie Lhihane Llama Lorrie Lt. Lucy Lyle Madeira Mechanic Mg. Minnie Morrie Mr. Ms. Mt. Music My Nanny Nellie Nillie Novocane Null Nyack Oak Oblique Occarina Odd Oedipus Off Ogmane Ohio Oil Oj Oklahoma Olio Omni Only Oops Opera Oqu Order Ostra Ottmar Out Ovum Ow Ox Oyster Oz Parade Pd. Pepe Pfister Pg. Phil Pippi Pj Please Pneumonia Porridge Price Psalm Pt. Purple Pv Pw Pyre Qt. Quincy Radio Rd. Red Rhea Right Rj Roche Rr Rs Rt. Rural Rwanda Ryder Sacrifice Series Sgraffito Shirt Sister Skeet Slow Smore Snoop Soon Special Squire Sr St. Suzy Svelte Swiss Sy Szach Td Teach There Title Total Trust Tsena Tulip Twice Tyler Tzean Ua Udder Ue Uf Ugh Uh Ui Uk Ul Um Unkempt Uo Up Uq Ursula Use Utmost Uvula Uw Uxurious Uzßai Valerie Velour Vh Vicky Volvo Vs Water Were Where With World Wt. Wulk Wyler Xavier Xerox Xi Xylophone Yaboe Year Yipes Yo Ypsilant Ys Yu Zabar’s Zero Zhane Zizi Zorro Zu Zy Don’t I’ll I’m I’se"

misc_text = """Raptor's Blackbird micro-ATX POWER9 System Is Ready To Take Flight This Week
Written by Michael Larabel in Hardware on 19 May 2019 at 08:00 AM EDT. 19 Comments
The Raptor Blackbird supports up to 8-core 160W Sforza POWER9 CPUs, two DDR4 ECC modules, one PCI Express 4.0 x16 slot (and one PCIe 4.0 x8), dual Gigabit Ethernet, 4 x SATA 3.0 ports, four USB 3.0 ports, and other standard connectivity.
As I mentioned in my talk at Scale 17x
NetBSD 8.1 RC1 Released With MDS Mitigations, Option To Turn Off SMT/HT, Driver Updates
RadeonSI Primitive Culling Lands In Mesa 19.2
Lenovo Hooks Up With Debian For DebConf 19
Xfce 4.14 Sees Its Long-Awaited Pre-Release
Linux 5.2-rc1 Kernel Released With Case-Insensitive EXT4, New Intel HW & RTW88 WiFi
Linux's vmalloc Seeing "Large Performance Benefits" With 5.2 Kernel Changes
SVT-AV1 0.5 Released As Intel's Speedy AV1 Video Encoder
DXVK 1.2.1 Released With Game Fixes, Some Performance Improvements
LibreOffice 6.3 Alpha Was Tagged This Week, Stable Expected In August
Raptor's Blackbird micro-ATX POWER9 System Is Ready To Take Flight This Week
A Look At The MDS Cost On Xeon, EPYC & Xeon Total Impact Of Affected CPU Vulnerabilities
The Many Changes & Additions To Find With The Linux 5.2 Kernel
The Performance Impact Of MDS / Zombieload Plus The Overall Cost Now Of Spectre/Meltdown/L1TF/MDS
GeForce GTX 650 vs. GTX 1650 Performance For Linux Gaming, Performance-Per-Watt
GCC 9 vs. Clang 8 C/C++ Compiler Performance On AMD Threadripper, Intel Core i9
In the development branch (leading up to 3.34 this autumn) supported in GTK 4 from a 3.30.x version.
Radeon ROCm 2.5 Released With rocThrust, AMD Infinity Fabric Link Support
Ubuntu Touch Nearing Updated Unity 8 + Mir, But Not Yet Full Wayland
AMD GCN Back-End In GCC Compiler Adds "-march=gfx906" Option For Vega 20
RPM 4.15 With Better Performance & New Features Will Make It Into Fedora 31
FreeBSD 11.3 Beta 3 Arrives With Various Fixes, Correct Battery Life Reporting
Git 2.22 Released With Improvements Around Merge Handling, Other Small Enhancements
WineD3D Optimistic In Their Yet To Be Proven Vulkan Backend, DXVK "Dead End"
NVIDIA Firmware Blobs Get Updated To Help Some Pascal GPUs With Nouveau
A Last Call To Celebrate Phoronix's 15th Birthday By Going Premium
A Look At How The Linux Performance Has Evolved Since The AMD EPYC Launch
LLVM/Clang 9.0 Merges Support For Intel "Cooperlake" CPU Target
Mesa 19.2 RADV Driver Now Fully Supports EXT_sample_locations For Possible AA Benefits
SUSE Reworking Btrfs File-System's Locking Code
Amlogic Video Decode Driver Revised A Ninth Time In Pursuit Of The Linux Kernel
Proton 4.2-6  Brings DXVK 1.2.1 Rebuild, Updated FAudio, Other Fixes
LLVM's New Fortran Compiler Previously Called "f18" Will Take The Name Of Flang
RHEL 7.7 Beta Comes With MDS/Zombieload Mitigations
Google Stadia's E3 Event Reveals New Details For This Linux+Vulkan Gaming Service
Benchmarking Five ~$30 USD Solid-State Drives Under Ubuntu Linux
Mesa 19.2 Now Exposes The NVIDIA-Led EGL_EXT_platform_device Support
GNOME 3.34's Mutter Adds Mouse Accessibility Support For X11/Wayland
Benchmarks Of The Various Kernel Flavors Of Clear Linux
Ubuntu Moving Ahead With Compressing Their Kernel Image Using LZ4
QtCoAP Added To Qt 5.13 To Increase Its Relevance For Internet of Things
KDE Has Made Much Progress On Usability/Productivity, But They're Still Aiming For More
Debian's Anti-Harassment Team Continues Battling Community Issues In 2019
Alyssa Rosenzweig Joins Collabora To Work On Panfrost Graphics Stack
Intel Core i5 8400 vs. i5 9400F Meltdown/Spectre/L1TF/MDS Mitigation Impact
AMD Sends In 2nd Round Of AMDGPU Radeon Driver Updates For Linux 5.3 - No Navi Yet
Purism Talks Up The Librem 5 Smartphone Boot Speed, Price Increase Coming
Mesa 19.1-RC5 Is Out With A Handful Of RADV & Intel/Iris Changes
ATI R300 Gallium3D Driver Seeing A Big Performance Fix After Being Regressed For Years"""

cantarell = installFont("/tmp/Cantarell-VF.otf")

format = "A4Landscape"
border = 25
gutter = border * 0.5
pageWidth, pageHeight = sizes(format)
boxWidth = pageWidth - border * 2
boxHeight = pageHeight - border * 2

newPage(format)
font(cantarell)
fontVariations(wght=100)
fontSize(20)
textBox(basic_test, (border, border, boxWidth, boxHeight))

newPage(format)
font(cantarell)
fontVariations(wght=100)
fontSize(13)
textBox(lc_text + "\n\n" + uc_text, (border, border, boxWidth, boxHeight))

newPage(format)
font(cantarell)
fontVariations(wght=100)
fontSize(13)
textBox(ul_text+ "\n\n" + misc_text, (border, border, boxWidth, boxHeight))
