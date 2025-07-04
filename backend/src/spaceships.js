import * as THREE from 'three';

export function createSpaceship(canvas, shipType) {
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });

    renderer.setSize(canvas.clientWidth, canvas.clientHeight);
    renderer.setClearColor(0x000000, 0);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    let shipGroup;

    switch (shipType) {
        case 'x-wing':
            shipGroup = createXWing();
            break;
        case 'millennium-falcon':
            shipGroup = createMillenniumFalcon();
            break;
        case 'star-destroyer':
            shipGroup = createStarDestroyer();
            break;
        case 'nova-cruiser':
            shipGroup = createNovaCruiser();
            break;
        default:
            shipGroup = createXWing();
    }

    scene.add(shipGroup);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xff6b35, 1.2);
    directionalLight.position.set(5, 5, 5);
    directionalLight.castShadow = true;
    scene.add(directionalLight);

    const pointLight = new THREE.PointLight(0xffffff, 0.8, 50);
    pointLight.position.set(-3, 3, 3);
    scene.add(pointLight);

    // Camera position
    camera.position.set(4, 2, 4);
    camera.lookAt(0, 0, 0);

    // Animation
    let time = 0;
    function animate() {
        requestAnimationFrame(animate);
        time += 0.01;

        shipGroup.rotation.y += 0.005;
        shipGroup.position.y = Math.sin(time * 0.8) * 0.1;

        renderer.render(scene, camera);
    }

    animate();

    // Handle resize
    function handleResize() {
        const width = canvas.clientWidth;
        const height = canvas.clientHeight;
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
    }

    window.addEventListener('resize', handleResize);

    return { scene, camera, renderer, shipGroup };
}

function createXWing() {
    const group = new THREE.Group();

    const bodyMaterial = new THREE.MeshPhongMaterial({ color: 0xcccccc, shininess: 100 });
    const wingMaterial = new THREE.MeshPhongMaterial({ color: 0xaaaaaa, shininess: 80 });
    const engineMaterial = new THREE.MeshPhongMaterial({ color: 0x666666, shininess: 120 });

    const bodyGeometry = new THREE.CylinderGeometry(0.2, 0.3, 2.5, 8);
    const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
    body.rotation.z = Math.PI / 2;
    body.castShadow = true;
    group.add(body);

    const wingGeometry = new THREE.BoxGeometry(2, 0.15, 0.5);
    const wings = [
        { x: 0, y: 0.8, z: 0.3 },
        { x: 0, y: -0.8, z: 0.3 },
        { x: 0, y: 0.8, z: -0.3 },
        { x: 0, y: -0.8, z: -0.3 }
    ];
    wings.forEach(pos => {
        const wing = new THREE.Mesh(wingGeometry, wingMaterial);
        wing.position.set(pos.x, pos.y, pos.z);
        wing.castShadow = true;
        group.add(wing);
    });

    const engineGeometry = new THREE.CylinderGeometry(0.08, 0.12, 0.4, 8);
    const engines = [
        { x: -1.2, y: 0.8, z: 0.3 },
        { x: -1.2, y: -0.8, z: 0.3 },
        { x: -1.2, y: 0.8, z: -0.3 },
        { x: -1.2, y: -0.8, z: -0.3 }
    ];
    engines.forEach(pos => {
        const engine = new THREE.Mesh(engineGeometry, engineMaterial);
        engine.position.set(pos.x, pos.y, pos.z);
        engine.rotation.z = Math.PI / 2;
        engine.castShadow = true;
        group.add(engine);
    });
    
    group.scale.set(1.8, 1.2 ,1.2);

    return group;
}

function createMillenniumFalcon() {
    const group = new THREE.Group();

    const hullMaterial = new THREE.MeshPhongMaterial({ color: 0xbbbbbb, shininess: 60 });
    const detailMaterial = new THREE.MeshPhongMaterial({ color: 0x888888, shininess: 80 });

    const hullGeometry = new THREE.CylinderGeometry(1.2, 1.2, 0.3, 16);
    const hull = new THREE.Mesh(hullGeometry, hullMaterial);
    hull.castShadow = true;
    group.add(hull);

    const cockpitGeometry = new THREE.BoxGeometry(0.6, 0.8, 0.4);
    const cockpit = new THREE.Mesh(cockpitGeometry, detailMaterial);
    cockpit.position.set(0.8, 0, 0.2);
    cockpit.castShadow = true;
    group.add(cockpit);

    const mandibleGeometry = new THREE.BoxGeometry(0.8, 0.3, 0.2);
    const leftMandible = new THREE.Mesh(mandibleGeometry, hullMaterial);
    leftMandible.position.set(1.2, 0.5, 0);
    leftMandible.castShadow = true;
    group.add(leftMandible);

    const rightMandible = new THREE.Mesh(mandibleGeometry, hullMaterial);
    rightMandible.position.set(1.2, -0.5, 0);
    rightMandible.castShadow = true;
    group.add(rightMandible);

    const engineGeometry = new THREE.CylinderGeometry(0.15, 0.2, 0.3, 8);
    const engine1 = new THREE.Mesh(engineGeometry, detailMaterial);
    engine1.position.set(-0.8, 0.4, -0.2);
    engine1.castShadow = true;
    group.add(engine1);

    const engine2 = new THREE.Mesh(engineGeometry, detailMaterial);
    engine2.position.set(-0.8, -0.4, -0.2);
    engine2.castShadow = true;
    group.add(engine2);
    group.scale.set(1.8, 2,1.2);
    return group;
}

function createStarDestroyer() {
    const group = new THREE.Group();

    const hullMaterial = new THREE.MeshPhongMaterial({ color: 0x999999, shininess: 80 });
    const detailMaterial = new THREE.MeshPhongMaterial({ color: 0x666666, shininess: 100 });

    const hullGeometry = new THREE.ConeGeometry(1.5, 3, 3);
    const hull = new THREE.Mesh(hullGeometry, hullMaterial);
    hull.rotation.z = Math.PI / 2;
    hull.castShadow = true;
    group.add(hull);

    const bridgeGeometry = new THREE.BoxGeometry(0.3, 0.3, 0.8);
    const bridge = new THREE.Mesh(bridgeGeometry, detailMaterial);
    bridge.position.set(-0.5, 0, 0.5);
    bridge.castShadow = true;
    group.add(bridge);

    const engineGeometry = new THREE.BoxGeometry(0.8, 1.2, 0.4);
    const engines = new THREE.Mesh(engineGeometry, detailMaterial);
    engines.position.set(-1.2, 0, 0);
    engines.castShadow = true;
    group.add(engines);

    const detailGeometry = new THREE.BoxGeometry(0.2, 0.6, 0.2);
    for (let i = 0; i < 4; i++) {
        const detail = new THREE.Mesh(detailGeometry, detailMaterial);
        detail.position.set(0.5 - i * 0.3, (i % 2 === 0 ? 0.3 : -0.3), 0.2);
        detail.castShadow = true;
        group.add(detail);
    }
    group.scale.set(1.4, 1.4,1.2);

    return group;
}

function createNovaCruiser() {
    const group = new THREE.Group();

    const bodyMaterial = new THREE.MeshPhongMaterial({ color: 0x3a9ad9, shininess: 100 });
    const wingMaterial = new THREE.MeshPhongMaterial({ color: 0x2e6da4, shininess: 90 });
    const engineMaterial = new THREE.MeshPhongMaterial({ color: 0xff6600, emissive: 0xff3300, shininess: 200 });

    const hullGeometry = new THREE.CylinderGeometry(0.2, 0.5, 3, 16);
    const hull = new THREE.Mesh(hullGeometry, bodyMaterial);
    hull.rotation.z = Math.PI / 2;
    hull.castShadow = true;
    group.add(hull);

    const cockpitGeometry = new THREE.SphereGeometry(0.3, 16, 16);
    const cockpit = new THREE.Mesh(cockpitGeometry, new THREE.MeshPhongMaterial({ color: 0x66ccff, transparent: true, opacity: 0.7 }));
    cockpit.position.set(1.2, 0, 0.3);
    cockpit.castShadow = true;
    group.add(cockpit);

    const wingGeometry = new THREE.BoxGeometry(2.5, 0.1, 0.5);
    const leftWing = new THREE.Mesh(wingGeometry, wingMaterial);
    leftWing.position.set(0, 1, 0);
    leftWing.castShadow = true;
    group.add(leftWing);

    const rightWing = new THREE.Mesh(wingGeometry, wingMaterial);
    rightWing.position.set(0, -1, 0);
    rightWing.castShadow = true;
    group.add(rightWing);

    const engineGeometry = new THREE.CylinderGeometry(0.1, 0.2, 0.6, 12);
    const engine1 = new THREE.Mesh(engineGeometry, engineMaterial);
    engine1.rotation.z = Math.PI / 2;
    engine1.position.set(-1.6, 0.5, 0);
    engine1.castShadow = true;

    const engine2 = new THREE.Mesh(engineGeometry, engineMaterial);
    engine2.rotation.z = Math.PI / 2;
    engine2.position.set(-1.6, -0.5, 0);
    engine2.castShadow = true;

    group.add(engine1);
    group.add(engine2);

    return group;
}
