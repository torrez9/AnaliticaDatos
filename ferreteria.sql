-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 19-03-2026 a las 03:18:17
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `ferreteria`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `abono_clientes`
--

CREATE TABLE `abono_clientes` (
  `Id_abonocliente` bigint(20) UNSIGNED NOT NULL,
  `Id_cuentacobrar` bigint(20) UNSIGNED NOT NULL,
  `Idusuario` bigint(20) UNSIGNED NOT NULL,
  `Id_tipopago` bigint(20) UNSIGNED NOT NULL,
  `Referencia` varchar(255) NOT NULL,
  `Num_abono` int(11) NOT NULL,
  `Fecha` date NOT NULL,
  `Monto_abono` decimal(10,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `abono_proveedors`
--

CREATE TABLE `abono_proveedors` (
  `Id_abonoprov` bigint(20) UNSIGNED NOT NULL,
  `Id_cuentapagar` bigint(20) UNSIGNED NOT NULL,
  `Id_tipopago` bigint(20) UNSIGNED NOT NULL,
  `Idusuario` bigint(20) UNSIGNED DEFAULT NULL,
  `Referencia` varchar(255) NOT NULL,
  `Num_abono` int(11) NOT NULL,
  `Fecha` date NOT NULL,
  `Monto_abono` decimal(10,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `bodegas`
--

CREATE TABLE `bodegas` (
  `Idbodega` bigint(20) UNSIGNED NOT NULL,
  `Nombre_bodega` varchar(255) NOT NULL,
  `Direccion` varchar(255) DEFAULT NULL,
  `Idsucursal` bigint(20) UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cache`
--

CREATE TABLE `cache` (
  `key` varchar(255) NOT NULL,
  `value` mediumtext NOT NULL,
  `expiration` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cache_locks`
--

CREATE TABLE `cache_locks` (
  `key` varchar(255) NOT NULL,
  `owner` varchar(255) NOT NULL,
  `expiration` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `Idcategoria` bigint(20) UNSIGNED NOT NULL,
  `Nombre_cat` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `Idcliente` bigint(20) UNSIGNED NOT NULL,
  `Cedula` varchar(255) DEFAULT NULL,
  `Nombre` varchar(255) NOT NULL,
  `Apellido` varchar(255) NOT NULL,
  `Telefono` varchar(255) DEFAULT NULL,
  `Correo` varchar(255) DEFAULT NULL,
  `Limitecredito` decimal(10,2) DEFAULT NULL,
  `Saldocredito` decimal(10,2) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cotizacions`
--

CREATE TABLE `cotizacions` (
  `Id_Cotizacion` bigint(20) UNSIGNED NOT NULL,
  `Idcliente` bigint(20) UNSIGNED NOT NULL,
  `Idusuario` bigint(20) UNSIGNED NOT NULL,
  `Estado` varchar(255) DEFAULT NULL,
  `Fecha` datetime NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `Descuento` decimal(10,2) NOT NULL,
  `Total` decimal(10,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cuentas_cobrars`
--

CREATE TABLE `cuentas_cobrars` (
  `Id_cuentacobrar` bigint(20) UNSIGNED NOT NULL,
  `IdFactura` bigint(20) UNSIGNED NOT NULL,
  `Idcliente` bigint(20) UNSIGNED NOT NULL,
  `Estado` varchar(255) NOT NULL,
  `Fecha_emision` date NOT NULL,
  `Fecha_vencimiento` date NOT NULL,
  `Saldo_pendiente` decimal(10,2) NOT NULL,
  `Total` decimal(10,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cuentas_pagars`
--

CREATE TABLE `cuentas_pagars` (
  `Id_cuentapagar` bigint(20) UNSIGNED NOT NULL,
  `Idrecepcion` bigint(20) UNSIGNED NOT NULL,
  `Idproveedor` bigint(20) UNSIGNED NOT NULL,
  `Estado` varchar(255) NOT NULL,
  `Fecha_emision` date NOT NULL,
  `Fecha_vencimiento` date NOT NULL,
  `Saldo_pendiente` decimal(10,2) NOT NULL,
  `Total` decimal(10,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_cots`
--

CREATE TABLE `detalle_cots` (
  `Id_detallecot` bigint(20) UNSIGNED NOT NULL,
  `Id_Cotizacion` bigint(20) UNSIGNED NOT NULL,
  `Idproducto` bigint(20) UNSIGNED DEFAULT NULL,
  `Idkit` bigint(20) UNSIGNED DEFAULT NULL,
  `Cantidad` decimal(10,2) NOT NULL,
  `Precio` decimal(10,2) NOT NULL,
  `Descuento` decimal(10,2) NOT NULL,
  `Tipo_precio` varchar(255) NOT NULL,
  `Importe` decimal(10,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_devs`
--

CREATE TABLE `detalle_devs` (
  `Id_detalledev` bigint(20) UNSIGNED NOT NULL,
  `Id_devolucion` bigint(20) UNSIGNED NOT NULL,
  `Id_detallefac` bigint(20) UNSIGNED NOT NULL,
  `Cantidad_dev` decimal(10,2) NOT NULL,
  `Precio` decimal(10,2) NOT NULL,
  `Subtotal_dev` decimal(10,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_facs`
--

CREATE TABLE `detalle_facs` (
  `Id_detallefac` bigint(20) UNSIGNED NOT NULL,
  `IdFactura` bigint(20) UNSIGNED NOT NULL,
  `Idproducto` bigint(20) UNSIGNED DEFAULT NULL,
  `Idbodega` bigint(20) UNSIGNED NOT NULL,
  `Idkit` bigint(20) UNSIGNED DEFAULT NULL,
  `Producto_Gen` varchar(255) DEFAULT NULL,
  `Cantidad` decimal(10,2) NOT NULL,
  `Descuento` decimal(10,2) NOT NULL,
  `Precio` decimal(10,2) NOT NULL,
  `Importe` decimal(10,2) NOT NULL,
  `Devolucion` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_invs`
--

CREATE TABLE `detalle_invs` (
  `Id_detalleinv` bigint(20) UNSIGNED NOT NULL,
  `Id_inventario` bigint(20) UNSIGNED NOT NULL,
  `Idproducto` bigint(20) UNSIGNED NOT NULL,
  `Cantidad` decimal(10,2) NOT NULL,
  `Min_stock` int(11) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_kits`
--

CREATE TABLE `detalle_kits` (
  `Id_detallekit` bigint(20) UNSIGNED NOT NULL,
  `Idkit` bigint(20) UNSIGNED NOT NULL,
  `Idproducto` bigint(20) UNSIGNED NOT NULL,
  `Cantidad` decimal(10,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_movs`
--

CREATE TABLE `detalle_movs` (
  `Id_detallemov` bigint(20) UNSIGNED NOT NULL,
  `Id_movimiento` bigint(20) UNSIGNED NOT NULL,
  `Idproducto` bigint(20) UNSIGNED NOT NULL,
  `Idbodega_origen` bigint(20) UNSIGNED DEFAULT NULL,
  `Idbodega_destino` bigint(20) UNSIGNED DEFAULT NULL,
  `Cantidad` decimal(10,2) NOT NULL,
  `Importe_mov` decimal(10,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_recs`
--

CREATE TABLE `detalle_recs` (
  `Id_detallerecep` bigint(20) UNSIGNED NOT NULL,
  `Idrecepcion` bigint(20) UNSIGNED NOT NULL,
  `Idproducto` bigint(20) UNSIGNED NOT NULL,
  `Idbodega` bigint(20) UNSIGNED DEFAULT NULL,
  `Id_tipopago` bigint(20) UNSIGNED NOT NULL,
  `Cantidad` decimal(10,2) NOT NULL,
  `Precio_costo` decimal(10,2) NOT NULL,
  `Importe` decimal(10,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `devoluciones`
--

CREATE TABLE `devoluciones` (
  `Id_devolucion` bigint(20) UNSIGNED NOT NULL,
  `IdFactura` bigint(20) UNSIGNED NOT NULL,
  `Idusuario` bigint(20) UNSIGNED NOT NULL,
  `Fecha_dev` datetime NOT NULL,
  `Total_devuelto` decimal(10,2) NOT NULL,
  `Motivo` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `facturas`
--

CREATE TABLE `facturas` (
  `IdFactura` bigint(20) UNSIGNED NOT NULL,
  `Id_tipoentrega` bigint(20) UNSIGNED NOT NULL,
  `Id_tipopago` bigint(20) UNSIGNED NOT NULL,
  `Idusuario` bigint(20) UNSIGNED NOT NULL,
  `Idcliente` bigint(20) UNSIGNED NOT NULL,
  `Estado` varchar(255) NOT NULL,
  `Fecha` datetime NOT NULL,
  `Subtotal` decimal(10,2) NOT NULL,
  `Descuento` decimal(10,2) NOT NULL,
  `Total` decimal(10,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `failed_jobs`
--

CREATE TABLE `failed_jobs` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `uuid` varchar(255) NOT NULL,
  `connection` text NOT NULL,
  `queue` text NOT NULL,
  `payload` longtext NOT NULL,
  `exception` longtext NOT NULL,
  `failed_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventarios`
--

CREATE TABLE `inventarios` (
  `Id_inventario` bigint(20) UNSIGNED NOT NULL,
  `Idbodega` bigint(20) UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `jobs`
--

CREATE TABLE `jobs` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `queue` varchar(255) NOT NULL,
  `payload` longtext NOT NULL,
  `attempts` tinyint(3) UNSIGNED NOT NULL,
  `reserved_at` int(10) UNSIGNED DEFAULT NULL,
  `available_at` int(10) UNSIGNED NOT NULL,
  `created_at` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `job_batches`
--

CREATE TABLE `job_batches` (
  `id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `total_jobs` int(11) NOT NULL,
  `pending_jobs` int(11) NOT NULL,
  `failed_jobs` int(11) NOT NULL,
  `failed_job_ids` longtext NOT NULL,
  `options` mediumtext DEFAULT NULL,
  `cancelled_at` int(11) DEFAULT NULL,
  `created_at` int(11) NOT NULL,
  `finished_at` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `kits`
--

CREATE TABLE `kits` (
  `Idkit` bigint(20) UNSIGNED NOT NULL,
  `Nombre_kit` varchar(255) NOT NULL,
  `Precio_kit` decimal(10,2) DEFAULT NULL,
  `Estado` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `logs_sistema`
--

CREATE TABLE `logs_sistema` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED DEFAULT NULL,
  `accion` varchar(255) NOT NULL,
  `modulo` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `datos_antes` longtext DEFAULT NULL,
  `datos_despues` longtext DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `migrations`
--

CREATE TABLE `migrations` (
  `id` int(10) UNSIGNED NOT NULL,
  `migration` varchar(255) NOT NULL,
  `batch` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `movimientos`
--

CREATE TABLE `movimientos` (
  `Id_movimiento` bigint(20) UNSIGNED NOT NULL,
  `Idusuario` bigint(20) UNSIGNED NOT NULL,
  `Idproveedor` bigint(20) UNSIGNED DEFAULT NULL,
  `Motivo` varchar(255) DEFAULT NULL,
  `Tipo_mov` varchar(255) NOT NULL,
  `Total_Mov` decimal(10,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `password_reset_tokens`
--

CREATE TABLE `password_reset_tokens` (
  `email` varchar(255) NOT NULL,
  `token` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productoprovs`
--

CREATE TABLE `productoprovs` (
  `Id` bigint(20) UNSIGNED NOT NULL,
  `Idproveedor` bigint(20) UNSIGNED NOT NULL,
  `Idproducto` bigint(20) UNSIGNED NOT NULL,
  `Precio` decimal(10,2) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `Idproducto` bigint(20) UNSIGNED NOT NULL,
  `Idsubcat` bigint(20) UNSIGNED NOT NULL,
  `Id_Medida` bigint(20) UNSIGNED NOT NULL,
  `Codigo_barra` varchar(255) NOT NULL,
  `Nombre` varchar(255) NOT NULL,
  `foto` varchar(255) DEFAULT NULL,
  `Precio_costo` decimal(10,2) NOT NULL,
  `Precio_venta` decimal(10,2) NOT NULL,
  `Precio_descuento` decimal(10,2) NOT NULL,
  `Precio_Mayorista` decimal(10,2) NOT NULL,
  `Estado` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedors`
--

CREATE TABLE `proveedors` (
  `Idproveedor` bigint(20) UNSIGNED NOT NULL,
  `Razon_social` varchar(255) NOT NULL,
  `Telefono` varchar(255) NOT NULL,
  `Direccion` varchar(255) DEFAULT NULL,
  `Correo` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recepciones`
--

CREATE TABLE `recepciones` (
  `Idrecepcion` bigint(20) UNSIGNED NOT NULL,
  `Idproveedor` bigint(20) UNSIGNED NOT NULL,
  `Idusuario` bigint(20) UNSIGNED NOT NULL,
  `Id_tipopago` bigint(20) UNSIGNED NOT NULL,
  `Num_Factura` varchar(255) NOT NULL,
  `Fecha` datetime NOT NULL,
  `Estado` varchar(255) NOT NULL,
  `Subtotal` decimal(10,2) NOT NULL,
  `IVA` decimal(10,2) DEFAULT NULL,
  `Descuento` decimal(10,2) DEFAULT NULL,
  `Total` decimal(10,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rols`
--

CREATE TABLE `rols` (
  `Idrol` bigint(20) UNSIGNED NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sessions`
--

CREATE TABLE `sessions` (
  `id` varchar(255) NOT NULL,
  `user_id` bigint(20) UNSIGNED DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `payload` longtext NOT NULL,
  `last_activity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `subcategorias`
--

CREATE TABLE `subcategorias` (
  `Idsubcat` bigint(20) UNSIGNED NOT NULL,
  `Idcategoria` bigint(20) UNSIGNED NOT NULL,
  `Nombre_subcat` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sucursals`
--

CREATE TABLE `sucursals` (
  `Idsucursal` bigint(20) UNSIGNED NOT NULL,
  `Nombre_Sucursal` varchar(255) NOT NULL,
  `Direccion` varchar(255) DEFAULT NULL,
  `Gerente` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_entregas`
--

CREATE TABLE `tipo_entregas` (
  `Id_tipoentrega` bigint(20) UNSIGNED NOT NULL,
  `Descripcion` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_pagos`
--

CREATE TABLE `tipo_pagos` (
  `Id_tipopago` bigint(20) UNSIGNED NOT NULL,
  `Nombre_pago` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `unidadmedidas`
--

CREATE TABLE `unidadmedidas` (
  `Id_Medida` bigint(20) UNSIGNED NOT NULL,
  `Nombre_Medida` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `Idusuario` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `Apellido` varchar(255) DEFAULT NULL,
  `Usuario` varchar(255) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `email_verified_at` timestamp NULL DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `Estado` varchar(255) DEFAULT NULL,
  `Telefono` varchar(255) DEFAULT NULL,
  `foto_perfil` varchar(255) DEFAULT NULL,
  `Idrol` bigint(20) UNSIGNED DEFAULT NULL,
  `Comision` decimal(8,2) DEFAULT NULL,
  `remember_token` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `abono_clientes`
--
ALTER TABLE `abono_clientes`
  ADD PRIMARY KEY (`Id_abonocliente`),
  ADD KEY `abono_clientes_id_cuentacobrar_foreign` (`Id_cuentacobrar`),
  ADD KEY `abono_clientes_idusuario_foreign` (`Idusuario`),
  ADD KEY `abono_clientes_id_tipopago_foreign` (`Id_tipopago`);

--
-- Indices de la tabla `abono_proveedors`
--
ALTER TABLE `abono_proveedors`
  ADD PRIMARY KEY (`Id_abonoprov`),
  ADD KEY `abono_proveedors_id_cuentapagar_foreign` (`Id_cuentapagar`),
  ADD KEY `abono_proveedors_id_tipopago_foreign` (`Id_tipopago`);

--
-- Indices de la tabla `bodegas`
--
ALTER TABLE `bodegas`
  ADD PRIMARY KEY (`Idbodega`),
  ADD KEY `bodegas_idsucursal_foreign` (`Idsucursal`);

--
-- Indices de la tabla `cache`
--
ALTER TABLE `cache`
  ADD PRIMARY KEY (`key`);

--
-- Indices de la tabla `cache_locks`
--
ALTER TABLE `cache_locks`
  ADD PRIMARY KEY (`key`);

--
-- Indices de la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`Idcategoria`);

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`Idcliente`);

--
-- Indices de la tabla `cotizacions`
--
ALTER TABLE `cotizacions`
  ADD PRIMARY KEY (`Id_Cotizacion`),
  ADD KEY `cotizacions_idcliente_foreign` (`Idcliente`),
  ADD KEY `cotizacions_idusuario_foreign` (`Idusuario`);

--
-- Indices de la tabla `cuentas_cobrars`
--
ALTER TABLE `cuentas_cobrars`
  ADD PRIMARY KEY (`Id_cuentacobrar`),
  ADD KEY `cuentas_cobrars_idfactura_foreign` (`IdFactura`),
  ADD KEY `cuentas_cobrars_idcliente_foreign` (`Idcliente`);

--
-- Indices de la tabla `cuentas_pagars`
--
ALTER TABLE `cuentas_pagars`
  ADD PRIMARY KEY (`Id_cuentapagar`),
  ADD KEY `cuentas_pagars_idrecepcion_foreign` (`Idrecepcion`),
  ADD KEY `cuentas_pagars_idproveedor_foreign` (`Idproveedor`);

--
-- Indices de la tabla `detalle_cots`
--
ALTER TABLE `detalle_cots`
  ADD PRIMARY KEY (`Id_detallecot`),
  ADD KEY `detalle_cots_id_cotizacion_foreign` (`Id_Cotizacion`),
  ADD KEY `detalle_cots_idproducto_foreign` (`Idproducto`),
  ADD KEY `detalle_cots_idkit_foreign` (`Idkit`);

--
-- Indices de la tabla `detalle_devs`
--
ALTER TABLE `detalle_devs`
  ADD PRIMARY KEY (`Id_detalledev`),
  ADD KEY `detalle_devs_id_devolucion_foreign` (`Id_devolucion`),
  ADD KEY `detalle_devs_id_detallefac_foreign` (`Id_detallefac`);

--
-- Indices de la tabla `detalle_facs`
--
ALTER TABLE `detalle_facs`
  ADD PRIMARY KEY (`Id_detallefac`),
  ADD KEY `detalle_facs_idfactura_foreign` (`IdFactura`),
  ADD KEY `detalle_facs_idproducto_foreign` (`Idproducto`),
  ADD KEY `detalle_facs_idbodega_foreign` (`Idbodega`),
  ADD KEY `detalle_facs_idkit_foreign` (`Idkit`);

--
-- Indices de la tabla `detalle_invs`
--
ALTER TABLE `detalle_invs`
  ADD PRIMARY KEY (`Id_detalleinv`),
  ADD KEY `detalle_invs_id_inventario_foreign` (`Id_inventario`),
  ADD KEY `detalle_invs_idproducto_foreign` (`Idproducto`);

--
-- Indices de la tabla `detalle_kits`
--
ALTER TABLE `detalle_kits`
  ADD PRIMARY KEY (`Id_detallekit`),
  ADD KEY `detalle_kits_idkit_foreign` (`Idkit`),
  ADD KEY `detalle_kits_idproducto_foreign` (`Idproducto`);

--
-- Indices de la tabla `detalle_movs`
--
ALTER TABLE `detalle_movs`
  ADD PRIMARY KEY (`Id_detallemov`),
  ADD KEY `detalle_movs_id_movimiento_foreign` (`Id_movimiento`),
  ADD KEY `detalle_movs_idproducto_foreign` (`Idproducto`),
  ADD KEY `detalle_movs_idbodega_origen_foreign` (`Idbodega_origen`),
  ADD KEY `detalle_movs_idbodega_destino_foreign` (`Idbodega_destino`);

--
-- Indices de la tabla `detalle_recs`
--
ALTER TABLE `detalle_recs`
  ADD PRIMARY KEY (`Id_detallerecep`),
  ADD KEY `detalle_recs_idrecepcion_foreign` (`Idrecepcion`),
  ADD KEY `detalle_recs_idproducto_foreign` (`Idproducto`),
  ADD KEY `detalle_recs_idbodega_foreign` (`Idbodega`),
  ADD KEY `detalle_recs_id_tipopago_foreign` (`Id_tipopago`);

--
-- Indices de la tabla `devoluciones`
--
ALTER TABLE `devoluciones`
  ADD PRIMARY KEY (`Id_devolucion`),
  ADD KEY `devoluciones_idfactura_foreign` (`IdFactura`),
  ADD KEY `devoluciones_idusuario_foreign` (`Idusuario`);

--
-- Indices de la tabla `facturas`
--
ALTER TABLE `facturas`
  ADD PRIMARY KEY (`IdFactura`),
  ADD KEY `facturas_id_tipoentrega_foreign` (`Id_tipoentrega`),
  ADD KEY `facturas_id_tipopago_foreign` (`Id_tipopago`),
  ADD KEY `facturas_idusuario_foreign` (`Idusuario`),
  ADD KEY `facturas_idcliente_foreign` (`Idcliente`);

--
-- Indices de la tabla `failed_jobs`
--
ALTER TABLE `failed_jobs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `failed_jobs_uuid_unique` (`uuid`);

--
-- Indices de la tabla `inventarios`
--
ALTER TABLE `inventarios`
  ADD PRIMARY KEY (`Id_inventario`),
  ADD KEY `inventarios_idbodega_foreign` (`Idbodega`);

--
-- Indices de la tabla `jobs`
--
ALTER TABLE `jobs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `jobs_queue_index` (`queue`);

--
-- Indices de la tabla `job_batches`
--
ALTER TABLE `job_batches`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `kits`
--
ALTER TABLE `kits`
  ADD PRIMARY KEY (`Idkit`);

--
-- Indices de la tabla `logs_sistema`
--
ALTER TABLE `logs_sistema`
  ADD PRIMARY KEY (`id`),
  ADD KEY `logs_sistema_created_at_index` (`created_at`),
  ADD KEY `logs_sistema_user_id_index` (`user_id`),
  ADD KEY `logs_sistema_accion_index` (`accion`),
  ADD KEY `logs_sistema_modulo_index` (`modulo`);

--
-- Indices de la tabla `migrations`
--
ALTER TABLE `migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `movimientos`
--
ALTER TABLE `movimientos`
  ADD PRIMARY KEY (`Id_movimiento`),
  ADD KEY `movimientos_idusuario_foreign` (`Idusuario`),
  ADD KEY `movimientos_idproveedor_foreign` (`Idproveedor`);

--
-- Indices de la tabla `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  ADD PRIMARY KEY (`email`);

--
-- Indices de la tabla `productoprovs`
--
ALTER TABLE `productoprovs`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `productoprovs_idproveedor_foreign` (`Idproveedor`),
  ADD KEY `productoprovs_idproducto_foreign` (`Idproducto`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`Idproducto`),
  ADD UNIQUE KEY `productos_codigo_barra_unique` (`Codigo_barra`),
  ADD KEY `productos_idsubcat_foreign` (`Idsubcat`),
  ADD KEY `productos_id_medida_foreign` (`Id_Medida`);

--
-- Indices de la tabla `proveedors`
--
ALTER TABLE `proveedors`
  ADD PRIMARY KEY (`Idproveedor`);

--
-- Indices de la tabla `recepciones`
--
ALTER TABLE `recepciones`
  ADD PRIMARY KEY (`Idrecepcion`),
  ADD KEY `recepciones_idproveedor_foreign` (`Idproveedor`),
  ADD KEY `recepciones_idusuario_foreign` (`Idusuario`),
  ADD KEY `recepciones_id_tipopago_foreign` (`Id_tipopago`);

--
-- Indices de la tabla `rols`
--
ALTER TABLE `rols`
  ADD PRIMARY KEY (`Idrol`),
  ADD UNIQUE KEY `rols_nombre_unique` (`nombre`);

--
-- Indices de la tabla `sessions`
--
ALTER TABLE `sessions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sessions_user_id_index` (`user_id`),
  ADD KEY `sessions_last_activity_index` (`last_activity`);

--
-- Indices de la tabla `subcategorias`
--
ALTER TABLE `subcategorias`
  ADD PRIMARY KEY (`Idsubcat`),
  ADD KEY `subcategorias_idcategoria_foreign` (`Idcategoria`);

--
-- Indices de la tabla `sucursals`
--
ALTER TABLE `sucursals`
  ADD PRIMARY KEY (`Idsucursal`);

--
-- Indices de la tabla `tipo_entregas`
--
ALTER TABLE `tipo_entregas`
  ADD PRIMARY KEY (`Id_tipoentrega`);

--
-- Indices de la tabla `tipo_pagos`
--
ALTER TABLE `tipo_pagos`
  ADD PRIMARY KEY (`Id_tipopago`);

--
-- Indices de la tabla `unidadmedidas`
--
ALTER TABLE `unidadmedidas`
  ADD PRIMARY KEY (`Id_Medida`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`Idusuario`),
  ADD UNIQUE KEY `users_email_unique` (`email`),
  ADD KEY `users_idrol_foreign` (`Idrol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `abono_clientes`
--
ALTER TABLE `abono_clientes`
  MODIFY `Id_abonocliente` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `abono_proveedors`
--
ALTER TABLE `abono_proveedors`
  MODIFY `Id_abonoprov` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `bodegas`
--
ALTER TABLE `bodegas`
  MODIFY `Idbodega` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `categorias`
--
ALTER TABLE `categorias`
  MODIFY `Idcategoria` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `Idcliente` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cotizacions`
--
ALTER TABLE `cotizacions`
  MODIFY `Id_Cotizacion` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cuentas_cobrars`
--
ALTER TABLE `cuentas_cobrars`
  MODIFY `Id_cuentacobrar` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cuentas_pagars`
--
ALTER TABLE `cuentas_pagars`
  MODIFY `Id_cuentapagar` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `detalle_cots`
--
ALTER TABLE `detalle_cots`
  MODIFY `Id_detallecot` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `detalle_devs`
--
ALTER TABLE `detalle_devs`
  MODIFY `Id_detalledev` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `detalle_facs`
--
ALTER TABLE `detalle_facs`
  MODIFY `Id_detallefac` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `detalle_invs`
--
ALTER TABLE `detalle_invs`
  MODIFY `Id_detalleinv` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `detalle_kits`
--
ALTER TABLE `detalle_kits`
  MODIFY `Id_detallekit` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `detalle_movs`
--
ALTER TABLE `detalle_movs`
  MODIFY `Id_detallemov` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `detalle_recs`
--
ALTER TABLE `detalle_recs`
  MODIFY `Id_detallerecep` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `devoluciones`
--
ALTER TABLE `devoluciones`
  MODIFY `Id_devolucion` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `facturas`
--
ALTER TABLE `facturas`
  MODIFY `IdFactura` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `failed_jobs`
--
ALTER TABLE `failed_jobs`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inventarios`
--
ALTER TABLE `inventarios`
  MODIFY `Id_inventario` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `jobs`
--
ALTER TABLE `jobs`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `kits`
--
ALTER TABLE `kits`
  MODIFY `Idkit` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `logs_sistema`
--
ALTER TABLE `logs_sistema`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `migrations`
--
ALTER TABLE `migrations`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `movimientos`
--
ALTER TABLE `movimientos`
  MODIFY `Id_movimiento` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `productoprovs`
--
ALTER TABLE `productoprovs`
  MODIFY `Id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `Idproducto` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `proveedors`
--
ALTER TABLE `proveedors`
  MODIFY `Idproveedor` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `recepciones`
--
ALTER TABLE `recepciones`
  MODIFY `Idrecepcion` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `rols`
--
ALTER TABLE `rols`
  MODIFY `Idrol` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `subcategorias`
--
ALTER TABLE `subcategorias`
  MODIFY `Idsubcat` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `sucursals`
--
ALTER TABLE `sucursals`
  MODIFY `Idsucursal` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tipo_entregas`
--
ALTER TABLE `tipo_entregas`
  MODIFY `Id_tipoentrega` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tipo_pagos`
--
ALTER TABLE `tipo_pagos`
  MODIFY `Id_tipopago` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `unidadmedidas`
--
ALTER TABLE `unidadmedidas`
  MODIFY `Id_Medida` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `Idusuario` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `abono_clientes`
--
ALTER TABLE `abono_clientes`
  ADD CONSTRAINT `abono_clientes_id_cuentacobrar_foreign` FOREIGN KEY (`Id_cuentacobrar`) REFERENCES `cuentas_cobrars` (`Id_cuentacobrar`),
  ADD CONSTRAINT `abono_clientes_id_tipopago_foreign` FOREIGN KEY (`Id_tipopago`) REFERENCES `tipo_pagos` (`Id_tipopago`),
  ADD CONSTRAINT `abono_clientes_idusuario_foreign` FOREIGN KEY (`Idusuario`) REFERENCES `users` (`Idusuario`);

--
-- Filtros para la tabla `abono_proveedors`
--
ALTER TABLE `abono_proveedors`
  ADD CONSTRAINT `abono_proveedors_id_cuentapagar_foreign` FOREIGN KEY (`Id_cuentapagar`) REFERENCES `cuentas_pagars` (`Id_cuentapagar`),
  ADD CONSTRAINT `abono_proveedors_id_tipopago_foreign` FOREIGN KEY (`Id_tipopago`) REFERENCES `tipo_pagos` (`Id_tipopago`);

--
-- Filtros para la tabla `bodegas`
--
ALTER TABLE `bodegas`
  ADD CONSTRAINT `bodegas_idsucursal_foreign` FOREIGN KEY (`Idsucursal`) REFERENCES `sucursals` (`Idsucursal`);

--
-- Filtros para la tabla `cotizacions`
--
ALTER TABLE `cotizacions`
  ADD CONSTRAINT `cotizacions_idcliente_foreign` FOREIGN KEY (`Idcliente`) REFERENCES `clientes` (`Idcliente`),
  ADD CONSTRAINT `cotizacions_idusuario_foreign` FOREIGN KEY (`Idusuario`) REFERENCES `users` (`Idusuario`);

--
-- Filtros para la tabla `cuentas_cobrars`
--
ALTER TABLE `cuentas_cobrars`
  ADD CONSTRAINT `cuentas_cobrars_idcliente_foreign` FOREIGN KEY (`Idcliente`) REFERENCES `clientes` (`Idcliente`),
  ADD CONSTRAINT `cuentas_cobrars_idfactura_foreign` FOREIGN KEY (`IdFactura`) REFERENCES `facturas` (`IdFactura`);

--
-- Filtros para la tabla `cuentas_pagars`
--
ALTER TABLE `cuentas_pagars`
  ADD CONSTRAINT `cuentas_pagars_idproveedor_foreign` FOREIGN KEY (`Idproveedor`) REFERENCES `proveedors` (`Idproveedor`),
  ADD CONSTRAINT `cuentas_pagars_idrecepcion_foreign` FOREIGN KEY (`Idrecepcion`) REFERENCES `recepciones` (`Idrecepcion`);

--
-- Filtros para la tabla `detalle_cots`
--
ALTER TABLE `detalle_cots`
  ADD CONSTRAINT `detalle_cots_id_cotizacion_foreign` FOREIGN KEY (`Id_Cotizacion`) REFERENCES `cotizacions` (`Id_Cotizacion`),
  ADD CONSTRAINT `detalle_cots_idkit_foreign` FOREIGN KEY (`Idkit`) REFERENCES `kits` (`Idkit`),
  ADD CONSTRAINT `detalle_cots_idproducto_foreign` FOREIGN KEY (`Idproducto`) REFERENCES `productos` (`Idproducto`);

--
-- Filtros para la tabla `detalle_devs`
--
ALTER TABLE `detalle_devs`
  ADD CONSTRAINT `detalle_devs_id_detallefac_foreign` FOREIGN KEY (`Id_detallefac`) REFERENCES `detalle_facs` (`Id_detallefac`),
  ADD CONSTRAINT `detalle_devs_id_devolucion_foreign` FOREIGN KEY (`Id_devolucion`) REFERENCES `devoluciones` (`Id_devolucion`);

--
-- Filtros para la tabla `detalle_facs`
--
ALTER TABLE `detalle_facs`
  ADD CONSTRAINT `detalle_facs_idbodega_foreign` FOREIGN KEY (`Idbodega`) REFERENCES `bodegas` (`Idbodega`),
  ADD CONSTRAINT `detalle_facs_idfactura_foreign` FOREIGN KEY (`IdFactura`) REFERENCES `facturas` (`IdFactura`),
  ADD CONSTRAINT `detalle_facs_idkit_foreign` FOREIGN KEY (`Idkit`) REFERENCES `kits` (`Idkit`),
  ADD CONSTRAINT `detalle_facs_idproducto_foreign` FOREIGN KEY (`Idproducto`) REFERENCES `productos` (`Idproducto`);

--
-- Filtros para la tabla `detalle_invs`
--
ALTER TABLE `detalle_invs`
  ADD CONSTRAINT `detalle_invs_id_inventario_foreign` FOREIGN KEY (`Id_inventario`) REFERENCES `inventarios` (`Id_inventario`),
  ADD CONSTRAINT `detalle_invs_idproducto_foreign` FOREIGN KEY (`Idproducto`) REFERENCES `productos` (`Idproducto`);

--
-- Filtros para la tabla `detalle_kits`
--
ALTER TABLE `detalle_kits`
  ADD CONSTRAINT `detalle_kits_idkit_foreign` FOREIGN KEY (`Idkit`) REFERENCES `kits` (`Idkit`),
  ADD CONSTRAINT `detalle_kits_idproducto_foreign` FOREIGN KEY (`Idproducto`) REFERENCES `productos` (`Idproducto`);

--
-- Filtros para la tabla `detalle_movs`
--
ALTER TABLE `detalle_movs`
  ADD CONSTRAINT `detalle_movs_id_movimiento_foreign` FOREIGN KEY (`Id_movimiento`) REFERENCES `movimientos` (`Id_movimiento`),
  ADD CONSTRAINT `detalle_movs_idbodega_destino_foreign` FOREIGN KEY (`Idbodega_destino`) REFERENCES `bodegas` (`Idbodega`),
  ADD CONSTRAINT `detalle_movs_idbodega_origen_foreign` FOREIGN KEY (`Idbodega_origen`) REFERENCES `bodegas` (`Idbodega`),
  ADD CONSTRAINT `detalle_movs_idproducto_foreign` FOREIGN KEY (`Idproducto`) REFERENCES `productos` (`Idproducto`);

--
-- Filtros para la tabla `detalle_recs`
--
ALTER TABLE `detalle_recs`
  ADD CONSTRAINT `detalle_recs_id_tipopago_foreign` FOREIGN KEY (`Id_tipopago`) REFERENCES `tipo_pagos` (`Id_tipopago`),
  ADD CONSTRAINT `detalle_recs_idbodega_foreign` FOREIGN KEY (`Idbodega`) REFERENCES `bodegas` (`Idbodega`),
  ADD CONSTRAINT `detalle_recs_idproducto_foreign` FOREIGN KEY (`Idproducto`) REFERENCES `productos` (`Idproducto`),
  ADD CONSTRAINT `detalle_recs_idrecepcion_foreign` FOREIGN KEY (`Idrecepcion`) REFERENCES `recepciones` (`Idrecepcion`);

--
-- Filtros para la tabla `devoluciones`
--
ALTER TABLE `devoluciones`
  ADD CONSTRAINT `devoluciones_idfactura_foreign` FOREIGN KEY (`IdFactura`) REFERENCES `facturas` (`IdFactura`),
  ADD CONSTRAINT `devoluciones_idusuario_foreign` FOREIGN KEY (`Idusuario`) REFERENCES `users` (`Idusuario`);

--
-- Filtros para la tabla `facturas`
--
ALTER TABLE `facturas`
  ADD CONSTRAINT `facturas_id_tipoentrega_foreign` FOREIGN KEY (`Id_tipoentrega`) REFERENCES `tipo_entregas` (`Id_tipoentrega`),
  ADD CONSTRAINT `facturas_id_tipopago_foreign` FOREIGN KEY (`Id_tipopago`) REFERENCES `tipo_pagos` (`Id_tipopago`),
  ADD CONSTRAINT `facturas_idcliente_foreign` FOREIGN KEY (`Idcliente`) REFERENCES `clientes` (`Idcliente`),
  ADD CONSTRAINT `facturas_idusuario_foreign` FOREIGN KEY (`Idusuario`) REFERENCES `users` (`Idusuario`);

--
-- Filtros para la tabla `inventarios`
--
ALTER TABLE `inventarios`
  ADD CONSTRAINT `inventarios_idbodega_foreign` FOREIGN KEY (`Idbodega`) REFERENCES `bodegas` (`Idbodega`);

--
-- Filtros para la tabla `movimientos`
--
ALTER TABLE `movimientos`
  ADD CONSTRAINT `movimientos_idproveedor_foreign` FOREIGN KEY (`Idproveedor`) REFERENCES `proveedors` (`Idproveedor`),
  ADD CONSTRAINT `movimientos_idusuario_foreign` FOREIGN KEY (`Idusuario`) REFERENCES `users` (`Idusuario`);

--
-- Filtros para la tabla `productoprovs`
--
ALTER TABLE `productoprovs`
  ADD CONSTRAINT `productoprovs_idproducto_foreign` FOREIGN KEY (`Idproducto`) REFERENCES `productos` (`Idproducto`),
  ADD CONSTRAINT `productoprovs_idproveedor_foreign` FOREIGN KEY (`Idproveedor`) REFERENCES `proveedors` (`Idproveedor`);

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `productos_id_medida_foreign` FOREIGN KEY (`Id_Medida`) REFERENCES `unidadmedidas` (`Id_Medida`),
  ADD CONSTRAINT `productos_idsubcat_foreign` FOREIGN KEY (`Idsubcat`) REFERENCES `subcategorias` (`Idsubcat`);

--
-- Filtros para la tabla `recepciones`
--
ALTER TABLE `recepciones`
  ADD CONSTRAINT `recepciones_id_tipopago_foreign` FOREIGN KEY (`Id_tipopago`) REFERENCES `tipo_pagos` (`Id_tipopago`),
  ADD CONSTRAINT `recepciones_idproveedor_foreign` FOREIGN KEY (`Idproveedor`) REFERENCES `proveedors` (`Idproveedor`),
  ADD CONSTRAINT `recepciones_idusuario_foreign` FOREIGN KEY (`Idusuario`) REFERENCES `users` (`Idusuario`);

--
-- Filtros para la tabla `subcategorias`
--
ALTER TABLE `subcategorias`
  ADD CONSTRAINT `subcategorias_idcategoria_foreign` FOREIGN KEY (`Idcategoria`) REFERENCES `categorias` (`Idcategoria`);

--
-- Filtros para la tabla `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_idrol_foreign` FOREIGN KEY (`Idrol`) REFERENCES `rols` (`Idrol`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
