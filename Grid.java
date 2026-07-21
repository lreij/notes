package org.example;

import java.util.ArrayList;
import java.util.List;

public class Grid {

    public static void main(String[] args) {
        grid(10000, 1.486);
    }

    private static void grid(double quota, double initPrice) {
        List<Level> levels = new ArrayList<>();
        for (int i = 1; i < 20; i++) {
            double percent = 1 - i * 0.05;
            double rawPrice = initPrice * percent;
            double rawVolume = quota / rawPrice;
            double price = Math.round(rawPrice * 100) / 100.0;
            long volume = Math.round(rawVolume / 100) * 100;
            volume = getVolume(quota, price, volume);
            levels.add(new Level(percent, price, volume));
        }
        levels.forEach(System.out::println);
    }

    private static long getVolume(double quota, double price, long volume) {
        while (price * volume < quota) {
            volume += 100;
        }
        return volume;
    }

    static class Level {
        double percent;
        double price;
        long volume;

        Level(double percent, double price, long volume) {
            this.percent = percent;
            this.price = price;
            this.volume = volume;
        }

        @Override
        public String toString() {
            return String.format("%.2f %.2f %d %d", percent, price, volume, Math.round(price * volume));
        }
    }
}
