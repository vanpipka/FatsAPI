VESSELS_LIST = "SELECT" \
               "    vessels.name as name, " \
               "    vessels.id as id, " \
               "    vessels.imo as imo, " \
               "    vessels.mmsi as mmsi, " \
               "    vessels.marine_traffic_id as marine_traffic_id, "\
               "    COALESCE(areas.name, '') as area, " \
               "    COALESCE(max_date_coordinates.date, '0001-01-01 00:00:00.000') as refresh_date "\
               "FROM vessels as vessels " \
               "    LEFT JOIN (SELECT " \
               "            max(date) as date, " \
               "            vessel_id as vessel_id " \
               "        FROM coordinates " \
               "        GROUP BY vessel_id) as max_date_coordinates " \
               "    ON max_date_coordinates.vessel_id = vessels.id " \
               "    LEFT JOIN " \
               "        coordinates as last_coorfinates " \
               "    ON last_coorfinates.vessel_id = max_date_coordinates.vessel_id " \
               "        AND last_coorfinates.date = max_date_coordinates.date" \
               "    LEFT JOIN " \
               "        areas as areas " \
               "    ON areas.id = last_coorfinates.area_id "
